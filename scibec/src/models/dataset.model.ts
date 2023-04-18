import { belongsTo, hasMany, model, property } from '@loopback/repository';
import { Experiment, Scan } from '.';
import { SciBecEntity } from './scibecentity.model';

@model()
export class Dataset extends SciBecEntity {

  @property({
    type: 'string',
  })
  name?: string;

  @property({
    type: 'number',
  })
  number?: number;

  @hasMany(() => Scan, { keyTo: 'datasetId' })
  scans?: Scan[];

  @belongsTo(() => Experiment,
    {}, //relation metadata goes in here
    {// property definition goes in here
      mongodb: { dataType: 'ObjectId' }
    })
  experimentId?: string;

  constructor(data?: Partial<Dataset>) {
    super(data);
  }
}

export interface DatasetRelations {
  // describe navigational properties here
}

export type DatasetWithRelations = Dataset & DatasetRelations;
