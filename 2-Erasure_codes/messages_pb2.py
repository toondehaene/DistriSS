# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0emessages.proto\"%\n\x11storedata_request\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"`\n\x10\x64\x65legate_request\x12\x11\n\tfilenames\x18\x01 \x03(\t\x12\x14\n\x0cmax_erasures\x18\x02 \x01(\x05\x12\x11\n\tfile_size\x18\x03 \x01(\x05\x12\x10\n\x08\x65ncoding\x18\x04 \x01(\x08\"#\n\x0fgetdata_request\x12\x10\n\x08\x66ilename\x18\x01 \x01(\tb\x06proto3')



_STOREDATA_REQUEST = DESCRIPTOR.message_types_by_name['storedata_request']
_DELEGATE_REQUEST = DESCRIPTOR.message_types_by_name['delegate_request']
_GETDATA_REQUEST = DESCRIPTOR.message_types_by_name['getdata_request']
storedata_request = _reflection.GeneratedProtocolMessageType('storedata_request', (_message.Message,), {
  'DESCRIPTOR' : _STOREDATA_REQUEST,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:storedata_request)
  })
_sym_db.RegisterMessage(storedata_request)

delegate_request = _reflection.GeneratedProtocolMessageType('delegate_request', (_message.Message,), {
  'DESCRIPTOR' : _DELEGATE_REQUEST,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:delegate_request)
  })
_sym_db.RegisterMessage(delegate_request)

getdata_request = _reflection.GeneratedProtocolMessageType('getdata_request', (_message.Message,), {
  'DESCRIPTOR' : _GETDATA_REQUEST,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:getdata_request)
  })
_sym_db.RegisterMessage(getdata_request)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STOREDATA_REQUEST._serialized_start=18
  _STOREDATA_REQUEST._serialized_end=55
  _DELEGATE_REQUEST._serialized_start=57
  _DELEGATE_REQUEST._serialized_end=153
  _GETDATA_REQUEST._serialized_start=155
  _GETDATA_REQUEST._serialized_end=190
# @@protoc_insertion_point(module_scope)
