from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import os
import subprocess
from collections import OrderedDict
from hashlib import sha1

from twitter.common.collections import OrderedSet

from pants.backend.codegen.tasks.simple_codegen_task import SimpleCodegenTask
from pants.backend.jvm.targets.jar_library import JarLibrary
from pants.backend.jvm.targets.scala_library import ScalaLibrary
from pants.backend.jvm.tasks.jar_import_products import JarImportProducts
from pants.backend.jvm.tasks.nailgun_task import NailgunTask
from pants.base.build_environment import get_buildroot
from pants.base.exceptions import TaskError
from pants.build_graph.address import Address
from pants.fs.archive import ZIP
from scalapb.targets.scalapb_library import ScalaPBLibrary


class ScalaPBGen(SimpleCodegenTask, NailgunTask):
  def __init__(self, *args, **kwargs):
    super(ScalaPBGen, self).__init__(*args, **kwargs)

  @classmethod
  def register_options(cls, register):
    super(ScalaPBGen, cls).register_options(register)
    cls.register_jvm_tool(register, 'scalapbc')

  def synthetic_target_type(self, target):
    return ScalaLibrary

  def is_gentarget(self, target):
    return isinstance(target, ScalaPBLibrary)

  def execute_codegen(self, target, target_workdir):
    sources_by_base = self._calculate_sources(target)
    sources = target.sources_relative_to_buildroot()

    bases = OrderedSet(sources_by_base.keys())
    bases.update(self._proto_path_imports([target]))
    bases.update('.')

    gen_flag = '--scala_out'

    gen = '{0}={1}'.format(gen_flag, target_workdir)

    args = [gen]

    for base in bases:
      args.append('--proto_path={0}'.format(base))

    classpath = self.tool_classpath('scalapbc')

    args.extend(sources)
    main = 'com.trueaccord.scalapb.ScalaPBC'
    result = self.runjava(classpath=classpath, main=main, args=args, workunit_name='scalapb-gen')

    if result != 0:
      raise TaskError('scalapb-gen ... exited non-zero ({})'.format(result))

  def _calculate_sources(self, target):
    gentargets = OrderedSet()

    def add_to_gentargets(target):
      if self.is_gentarget(target):
        gentargets.add(target)
    self.context.build_graph.walk_transitive_dependency_graph(
      [target.address],
      add_to_gentargets,
      postorder=True)
    sources_by_base = OrderedDict()
    for target in gentargets:
      base = target.target_base
      if base not in sources_by_base:
        sources_by_base[base] = OrderedSet()
      sources_by_base[base].update(target.sources_relative_to_buildroot())
    return sources_by_base

  def _jars_to_directories(self, target):
    """Extracts and maps jars to directories containing their contents.

    :returns: a set of filepaths to directories containing the contents of jar.
    """
    files = set()
    jar_import_products = self.context.products.get_data(JarImportProducts)
    print ('jip', jar_import_products)
    imports = jar_import_products.imports(target)
    for coordinate, jar in imports:
      print ('jip', jar)
      files.add(self._extract_jar(coordinate, jar))
    return files

  def _extract_jar(self, coordinate, jar_path):
    """Extracts the jar to a subfolder of workdir/extracted and returns the path to it."""
    with open(jar_path, 'rb') as f:
      outdir = os.path.join(self.workdir, 'extracted', sha1(f.read()).hexdigest())
    if not os.path.exists(outdir):
      ZIP.extract(jar_path, outdir)
      self.context.log.debug('Extracting jar {jar} at {jar_path}.'
                             .format(jar=coordinate, jar_path=jar_path))
    else:
      self.context.log.debug('Jar {jar} already extracted at {jar_path}.'
                             .format(jar=coordinate, jar_path=jar_path))
    return outdir

  def _proto_path_imports(self, proto_targets):
    for target in proto_targets:
      for path in self._jars_to_directories(target):
        yield os.path.relpath(path, get_buildroot())

  @property
  def _copy_target_attributes(self):
    """Propagate the provides attribute to the synthetic java_library() target for publishing."""
    return ['provides']
