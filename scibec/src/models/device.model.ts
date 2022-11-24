import { belongsTo, Entity, hasMany, model, property } from '@loopback/repository';
import { Session } from '.';

export interface DeviceConfig {
  name?: string,
  label?: string
}

enum AcquisitionGroup {
  MOTOR = "motor",
  MONITOR = "monitor",
  STATUS = "status",
  DETECTOR = "detector",
}

enum AcquisitionPriority {
  PRIMARY = "primary",
  SECONDARY = "secondary",
  SKIP = "skip"
}

enum AcquisitionSchedule {
  SYNC = "sync",
  ASYNC = "async",
  FLYER = "flyer",
}

export interface AcquisitionConfig {
  schedule: AcquisitionSchedule,
  acquisitionGroup: AcquisitionGroup,
  readoutPriority: AcquisitionPriority
}

enum FailureType {
  RAISE = 'raise',
  RETRY = 'retry',
  BUFFER = 'buffer',
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

  @property.array(String, {
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
    jsonSchema: {
      properties: {
        schedule: {
          "description": "Acquisition scheduling.",
          "type": "string",
          "enum": ["sync", "async", "flyer"]
        },
        acquisitionGroup: {
          "description": "Type of device.",
          "type": "string",
          "enum": ["motor", "monitor", "status", "detector"],
        },
        readoutPriority: {
          "description": "Priority of the device during a scan.",
          "type": "string",
          "enum": ["primary", "secondary", "skip"],
        },
      },
      required: ["schedule", "acquisitionGroup", "readoutPriority"]
    },
    required: true,
    description: 'Config to determine the behaviour during data acquisition. Must include the fields schedule, readoutPriority and acquisitionGroup.',
  })
  acquisitionConfig: AcquisitionConfig;

  @property({
    type: 'string',
    jsonSchema: {
      enum: Object.values(FailureType),
    },
    description:
      'Defines how device failures are handled. "raise" raises an error immediately. "buffer" will try fall back to old values, should this not be possible, an error will be raised. "retry" will retry once before raising an error.',
    default: 'retry',
  })
  onFailure?: FailureType

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
