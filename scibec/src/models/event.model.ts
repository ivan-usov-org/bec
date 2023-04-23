import { belongsTo, model, property } from '@loopback/repository';
import { Device } from './device.model';
import { Scan } from './scan.model';
import { SciBecEntity } from './scibecentity.model';

@model()
export class Event extends SciBecEntity {
  @property({
    type: 'object',
  })
  data?: object;

  @belongsTo(() => Device,
    {}, //relation metadata goes in here
    {// property definition goes in here
      description: 'The events device',
      mongodb: { dataType: 'ObjectId' }
    })
  deviceId?: string;

  @belongsTo(() => Scan,
    {}, //relation metadata goes in here
    {// property definition goes in here
      description: 'The parent scan',
      mongodb: { dataType: 'ObjectId' }
    })
  scanId?: string;

  constructor(data?: Partial<Event>) {
    super(data);
  }
}

export interface EventRelations {
  // describe navigational properties here
}

export type EventWithRelations = Event & EventRelations;
