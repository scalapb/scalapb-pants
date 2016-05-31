from pants.build_graph.build_file_aliases import BuildFileAliases
from scalapb.targets.scalapb_library import ScalaPBLibrary
from scalapb.tasks.scalapb_gen import ScalaPBGen
from pants.goal.task_registrar import TaskRegistrar as task

def build_file_aliases():
    return BuildFileAliases(
        targets={
          'scalapb_library': ScalaPBLibrary,
        }
    )

def register_goals():
    task(name='scalapb_gen', action=ScalaPBGen).install('gen')

