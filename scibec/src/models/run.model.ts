import {Entity, model, property} from '@loopback/repository';

@model()
export class Run extends Entity {

  @property({
    type: 'string',
    id: true,
    generated: true,
    mongodb: {datatype: 'ObjectId'}
  })
  id?: string;

  @property({
    type: 'string',
  })
  ownerGroup?: string;

  @property({
    type: 'array',
    itemType: 'string',
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


  constructor(data?: Partial<Run>) {
    super(data);
  }
}

export interface RunRelations {
  // describe navigational properties here
}

export type RunWithRelations = Run & RunRelations;
