import simple.simple.SimpleMessage
import dep.dep.DependentProto

object Main {
  def main(args: Array[String]) = {
    val sm = SimpleMessage().update(_.number := 17)
    val dep = DependentProto().update(_.simpleField.number := 14)
    println(sm)
    println(dep)
  }
}
