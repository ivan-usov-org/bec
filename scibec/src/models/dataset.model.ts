import {belongsTo, Entity, model, property} from '@loopback/repository';
import {Scan} from '.';

@model()
export class Dataset extends Entity {
  @property({
    type: 'string',
    id: true,
    generated: true,
    mongodb: {datatype: 'ObjectId'}
  })
  id?: string;

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
    type: 'string',
  })
  name?: string;

  @property({
    type: 'date',
  })
  createdAt: Date;

  @property({
    type: 'string',
  })
  createdBy: string;

  @property({
    type: 'date',
  })
  updatedAt: Date;

  @property({
    type: 'string',
  })
  updatedBy: string;



  @belongsTo(() => Scan,
    {}, //relation metadata goes in here
    {// property definition goes in here
      mongodb: {dataType: 'ObjectId'}
    })
  scanId?: string;

  constructor(data?: Partial<Dataset>) {
    super(data);
  }
}

export interface DatasetRelations {
  // describe navigational properties here
}

export type DatasetWithRelations = Dataset & DatasetRelations;
