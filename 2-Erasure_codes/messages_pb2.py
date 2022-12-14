# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0emessages.proto\"$\n\x10\x66ragment_request\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"@\n\x15get_fragments_request\x12\x11\n\tfilenames\x18\x01 \x03(\t\x12\x14\n\x0cmax_erasures\x18\x02 \x01(\x05\"6\n\x11\x66ragments_reponse\x12\x11\n\tfilenames\x18\x01 \x03(\t\x12\x0e\n\x06\x63hunks\x18\x02 \x03(\x0c\"`\n\x10\x64\x65legate_request\x12\x11\n\tfilenames\x18\x01 \x03(\t\x12\x14\n\x0cmax_erasures\x18\x02 \x01(\x05\x12\x11\n\tfile_size\x18\x03 \x01(\x05\x12\x10\n\x08\x65ncoding\x18\x04 \x01(\x08\x62\x06proto3'
)




_FRAGMENT_REQUEST = _descriptor.Descriptor(
  name='fragment_request',
  full_name='fragment_request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filename', full_name='fragment_request.filename', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=54,
)


_GET_FRAGMENTS_REQUEST = _descriptor.Descriptor(
  name='get_fragments_request',
  full_name='get_fragments_request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filenames', full_name='get_fragments_request.filenames', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_erasures', full_name='get_fragments_request.max_erasures', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=56,
  serialized_end=120,
)


_FRAGMENTS_REPONSE = _descriptor.Descriptor(
  name='fragments_reponse',
  full_name='fragments_reponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filenames', full_name='fragments_reponse.filenames', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chunks', full_name='fragments_reponse.chunks', index=1,
      number=2, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=176,
)


_DELEGATE_REQUEST = _descriptor.Descriptor(
  name='delegate_request',
  full_name='delegate_request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filenames', full_name='delegate_request.filenames', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_erasures', full_name='delegate_request.max_erasures', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='file_size', full_name='delegate_request.file_size', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encoding', full_name='delegate_request.encoding', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=178,
  serialized_end=274,
)

DESCRIPTOR.message_types_by_name['fragment_request'] = _FRAGMENT_REQUEST
DESCRIPTOR.message_types_by_name['get_fragments_request'] = _GET_FRAGMENTS_REQUEST
DESCRIPTOR.message_types_by_name['fragments_reponse'] = _FRAGMENTS_REPONSE
DESCRIPTOR.message_types_by_name['delegate_request'] = _DELEGATE_REQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

fragment_request = _reflection.GeneratedProtocolMessageType('fragment_request', (_message.Message,), {
  'DESCRIPTOR' : _FRAGMENT_REQUEST,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:fragment_request)
  })
_sym_db.RegisterMessage(fragment_request)

get_fragments_request = _reflection.GeneratedProtocolMessageType('get_fragments_request', (_message.Message,), {
  'DESCRIPTOR' : _GET_FRAGMENTS_REQUEST,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:get_fragments_request)
  })
_sym_db.RegisterMessage(get_fragments_request)

fragments_reponse = _reflection.GeneratedProtocolMessageType('fragments_reponse', (_message.Message,), {
  'DESCRIPTOR' : _FRAGMENTS_REPONSE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:fragments_reponse)
  })
_sym_db.RegisterMessage(fragments_reponse)

delegate_request = _reflection.GeneratedProtocolMessageType('delegate_request', (_message.Message,), {
  'DESCRIPTOR' : _DELEGATE_REQUEST,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:delegate_request)
  })
_sym_db.RegisterMessage(delegate_request)


# @@protoc_insertion_point(module_scope)
