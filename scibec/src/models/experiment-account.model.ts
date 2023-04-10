import { belongsTo, model, property } from '@loopback/repository';
import { AccessAccount } from './access-account.model';
import { Experiment } from './experiment.model';

@model({
  settings: {
    strict: false,
    scope: {
      where: { isFunctional: false },
    },
    mongodb: { collection: 'AccessAccount' },
  },
})
export class ExperimentAccount extends AccessAccount {

  @property({
    type: 'boolean',
    default: false,
  })
  isFunctional: boolean;

  @belongsTo(() => Experiment,
    {}, //relation metadata goes in here
    {// property definition goes in here
      description: 'Experiment to which this account belongs.',
      mongodb: { dataType: 'ObjectId' }
    })
  experimentId?: string;

  constructor(data?: Partial<ExperimentAccount>) {
    super(data);
  }
}

export interface ExperimentAccountRelations {
  // describe navigational properties here
}

export type ExperimentAccountWithRelations = ExperimentAccount & ExperimentAccountRelations;
