import {inject} from '@loopback/core';
import {DefaultCrudRepository} from '@loopback/repository';
import {MongoDataSource} from '../datasources';
import {Run, RunRelations} from '../models';

export class RunRepository extends DefaultCrudRepository<
  Run,
  typeof Run.prototype.id,
  RunRelations
> {
  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
  ) {
    super(Run, dataSource);
  }
}
