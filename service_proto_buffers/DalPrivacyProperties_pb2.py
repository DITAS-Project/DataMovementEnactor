# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: DalPrivacyProperties.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='DalPrivacyProperties.proto',
  package='com.ditas.ehealth',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1a\x44\x61lPrivacyProperties.proto\x12\x11\x63om.ditas.ehealth\"\x88\x01\n\x14\x44\x61lPrivacyProperties\x12H\n\x0bprivacyZone\x18\x01 \x01(\x0e\x32\x33.com.ditas.ehealth.DalPrivacyProperties.PrivacyZone\"&\n\x0bPrivacyZone\x12\n\n\x06PUBLIC\x10\x00\x12\x0b\n\x07PRIVATE\x10\x01\x62\x06proto3')
)



_DALPRIVACYPROPERTIES_PRIVACYZONE = _descriptor.EnumDescriptor(
  name='PrivacyZone',
  full_name='com.ditas.ehealth.DalPrivacyProperties.PrivacyZone',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PUBLIC', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRIVATE', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=148,
  serialized_end=186,
)
_sym_db.RegisterEnumDescriptor(_DALPRIVACYPROPERTIES_PRIVACYZONE)


_DALPRIVACYPROPERTIES = _descriptor.Descriptor(
  name='DalPrivacyProperties',
  full_name='com.ditas.ehealth.DalPrivacyProperties',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='privacyZone', full_name='com.ditas.ehealth.DalPrivacyProperties.privacyZone', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DALPRIVACYPROPERTIES_PRIVACYZONE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=50,
  serialized_end=186,
)

_DALPRIVACYPROPERTIES.fields_by_name['privacyZone'].enum_type = _DALPRIVACYPROPERTIES_PRIVACYZONE
_DALPRIVACYPROPERTIES_PRIVACYZONE.containing_type = _DALPRIVACYPROPERTIES
DESCRIPTOR.message_types_by_name['DalPrivacyProperties'] = _DALPRIVACYPROPERTIES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DalPrivacyProperties = _reflection.GeneratedProtocolMessageType('DalPrivacyProperties', (_message.Message,), {
  'DESCRIPTOR' : _DALPRIVACYPROPERTIES,
  '__module__' : 'DalPrivacyProperties_pb2'
  # @@protoc_insertion_point(class_scope:com.ditas.ehealth.DalPrivacyProperties)
  })
_sym_db.RegisterMessage(DalPrivacyProperties)


# @@protoc_insertion_point(module_scope)
