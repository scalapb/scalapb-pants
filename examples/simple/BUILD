scalapb_library(
  name='simple_proto',
  sources=['./simple.proto'],
  dependencies=[
    '3rdparty/jvm:scalapb-runtime',
    '3rdparty/jvm:protobuf-runtime',
  ],
  java_conversions=True
)

scalapb_library(
  name='dep_proto',
  sources=['./dep.proto'],
  imports=[
  ],
  dependencies=[
    ':simple_proto',
    '3rdparty/jvm:scalapb-runtime'
  ]
)

jvm_binary(
  name='main',
  source='Main.scala',
  main='Main',
  dependencies=[':simple_proto', ':dep_proto'])
