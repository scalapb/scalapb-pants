package com.thesamet.scalapb.examples

import com.thesamet.scalapb.examples.simple.SimpleMessage
import com.thesamet.scalapb.examples.dep.DependentProto

object Main extends App {
  val sm = SimpleMessage().update(_.number := 17)
  val dep = DependentProto().update(_.simpleField.number := 14)
  println(sm)
  println(dep)
}
