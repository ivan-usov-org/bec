import { inject } from '@loopback/core';
import { MongoDataSource } from '../datasources';
import { Device, DeviceRelations } from '../models';
import { AutoAddRepository } from './autoadd.repository';

export class DeviceRepository extends AutoAddRepository<
  Device,
  typeof Device.prototype.id,
  DeviceRelations
> {
  constructor(
    @inject('datasources.mongo') dataSource: MongoDataSource,
  ) {
    super(Device, dataSource);
  }
}
