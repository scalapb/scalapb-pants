import com.trueaccord.scalapb.examples.simple.SimpleMessage
import com.trueaccord.scalapb.examples.dep.DependentProto

object Main {
  def main(args: Array[String]) = {
    val sm = SimpleMessage().update(_.number := 17)
    val dep = DependentProto().update(_.simpleField.number := 14)
    println(sm)
    println(dep)
  }
}
