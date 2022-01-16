from pants.build_graph.build_file_aliases import BuildFileAliases
from scalapb.pants.targets.scalapb_library import ScalaPBLibrary
from scalapb.pants.targets.target_types import ScalaPBLibraryTarget
from scalapb.pants.tasks.scalapb_gen import ScalaPBGen
from pants.goal.task_registrar import TaskRegistrar as task

def build_file_aliases():
    return BuildFileAliases(
        targets={
            ScalaPBLibrary.alias(): ScalaPBLibrary,
        }
    )

def register_goals():
    task(name='scalapb-gen', action=ScalaPBGen).install('gen')

def target_types():
    return [ScalaPBLibraryTarget]
