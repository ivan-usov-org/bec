import { inject } from '@loopback/core';
import { MongoDataSource } from '../datasources';
import { AccessAccount, AccessAccountRelations } from '../models';
import { AutoAddRepository } from './autoadd.repository';

export class AccessAccountRepository extends AutoAddRepository<
  AccessAccount,
  typeof AccessAccount.prototype.id,
  AccessAccountRelations
> {
  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
  ) {
    super(AccessAccount, dataSource);
  }
}
