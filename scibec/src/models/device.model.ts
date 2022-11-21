import { belongsTo, Entity, hasMany, model, property } from '@loopback/repository';
import { Session } from '.';

export interface DeviceConfig {
  name?: string,
  label?: string
}

export interface AcquisitionConfig {
  schedule: string,
  acquisitionGroup: string,
  onFailure: string
}

@model()
export class Device extends Entity {
  @property({
    type: 'string',
    id: true,
    generated: true,
    mongodb: { dataType: 'ObjectId' }
  })
  id: string;

  @property({
    type: 'string',
    required: true,
  })
  name: string;

  @property({
    type: 'string',
    required: false,
  })
  description: string;

  @property({
    type: 'string',
    description: 'Only members of the ownerGroup are allowed to modify this device'
  })
  ownerGroup?: string;

  @property.array(String, {
    description: 'groups whose members have read access to this device',
    index: true,
  })
  accessGroups?: string[];

  @property({
    type: 'date',
  })
  createdAt: Date;

  @property({
    type: 'string',
  })
  createdBy: string;


  @hasMany(() => Device, { keyTo: 'parentId' })
  subdevices?: Device[];

  @belongsTo(() => Device,
    {}, //relation metadata goes in here
    {// property definition goes in here
      mongodb: { dataType: 'ObjectId' }
    })
  parentId?: string;

  @belongsTo(() => Session,
    {}, //relation metadata goes in here
    {// property definition goes in here
      description: 'Session to which this device belongs.',
      mongodb: { dataType: 'ObjectId' }
    })
  sessionId?: string;

  @property({
    type: 'boolean',
    required: true,
    description: 'True if the device should be enabled.',
  })
  enabled: boolean;

  @property({
    type: 'boolean',
    required: false,
    description: 'True if the device is settable.',
  })
  enabled_set: boolean;

  @property({
    type: 'string',
    required: true,
    description: 'Ophyd device class',
  })
  deviceClass: string;

  @property({
    type: 'string',
    required: true,
    description: 'User-defined tags for easier access and grouping.',
  })
  deviceTags?: string[];

  @property({
    type: 'object',
    required: true,
    description: 'Device config, including the ophyd init arguments. Must at least contain name and label.',
  })
  deviceConfig: DeviceConfig;

  @property({
    type: 'object',
    required: true,
    description: 'Config to determine the behaviour during data acquisition. Must include the fields schedule and acquisitionGroup.',
  })
  acquisitionConfig: AcquisitionConfig;

  @property({
    type: 'object',
    required: false,
    description: 'Additional fields for user settings such as in and out positions.',
  })
  userParameter: object;



  constructor(data?: Partial<Device>) {
    super(data);
  }
}

export interface DeviceRelations {
  // describe navigational properties here
}

export type DeviceWithRelations = Device & DeviceRelations;
