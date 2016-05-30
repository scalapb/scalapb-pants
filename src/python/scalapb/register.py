from pants.build_graph.build_file_aliases import BuildFileAliases
from scalapb.targets.scalapb_library import ScalaPbLibrary
from scalapb.tasks.scalapb_gen import scalapb_gen
from pants.goal.task_registrar import TaskRegistrar as task

def build_file_aliases():
    return BuildFileAliases(
        targets={
          'scalapb_library': ScalaPbLibrary,
        }
    )

def register_goals():
    task(name='scalapb_gen', action=ScalaPBGen).install('gen')

