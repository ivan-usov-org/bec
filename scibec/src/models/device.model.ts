import {belongsTo, Entity, hasMany, model, property} from '@loopback/repository';
import {Session} from '.';

export interface DeviceConfig {
  name?: string,
  label?: string
}

export interface AcquisitionConfig {
  schedule?: string,
  maxFrequency?: number
}

@model()
export class Device extends Entity {
  @property({
    type: 'string',
    id: true,
    generated: true,
    mongodb: {dataType: 'ObjectId'}
  })
  id: string;

  @property({
    type: 'string',
    required: true,
  })
  name: string;

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

  @hasMany(() => Device, {keyTo: 'parentId'})
  subdevices?: Device[];

  @belongsTo(() => Device,
    {}, //relation metadata goes in here
    {// property definition goes in here
      mongodb: {dataType: 'ObjectId'}
    })
  parentId?: string;

  @belongsTo(() => Session,
    {}, //relation metadata goes in here
    {// property definition goes in here
      mongodb: {dataType: 'ObjectId'}
    })
  sessionId?: string;

  @property({
    type: 'boolean',
    required: true,
  })
  enabled: boolean;

  @property({
    type: 'string',
    required: true,
  })
  deviceClass: string;

  @property({
    type: 'string',
    required: true,
  })
  deviceGroup?: string;

  @property({
    type: 'object',
    required: true,
  })
  deviceConfig: DeviceConfig;

  @property({
    type: 'object',
    required: true,
  })
  acquisitionConfig: DeviceConfig;



  constructor(data?: Partial<Device>) {
    super(data);
  }
}

export interface DeviceRelations {
  // describe navigational properties here
}

export type DeviceWithRelations = Device & DeviceRelations;
