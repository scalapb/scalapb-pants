from pants.engine.target import (
    COMMON_TARGET_FIELDS,
    Dependencies,
    Sources,
    StringField,
    StringSequenceField,
    Target,
)

from pants.backend.jvm.target_types import (
  COMMON_JVM_FIELDS,
)

class Imports(StringSequenceField):
    alias = "imports"

class SourceRoot(StringField):
    alias = "source_root"

class ProtobufSources(Sources):
    default = ("*.proto",)
    expected_file_extensions = (".proto",)

class ScalaPBLibraryTarget(Target):
    """A Scala library generated from Protobuf IDL files."""

    alias = "scalapb_library"
    core_fields = (
        *COMMON_JVM_FIELDS,
       Imports,
       SourceRoot,
       ProtobufSources
    )
    v1_only = True
