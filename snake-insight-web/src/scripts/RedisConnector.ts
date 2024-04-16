import { createClient } from 'redis'
import { RedisClientType } from '@redis/client'

import { toRedisConnectUrl } from '@/scripts/formatTools'
import { type AttributeAddableObject } from '@/scripts/AttributeAddableObject'

type Options = 'NX' | 'XX'

type Types = 'string' | 'hash' | 'set'

export interface RedisConnectionConfig {
  host?: string,
  port?: number,
  user?: string,
  password?: string,
  database?: number
}

export interface KeyValuePair {
  key: string,
  type: Types,
  value: any,
  ttl: number
}

interface RedisBaseMethod {
  ping(): Promise<any>

  select(db: number): Promise<any>

  dbSize(): Promise<any>

  flushDb(): Promise<any>

  flushAll(): Promise<any>
}

interface RedisKeyMethod {
  keys(pattern: string): Promise<any>

  exists(key: string): Promise<any>

  del(...keys: string[]): Promise<any>

  type(key: string): Promise<any>

  expire(key: string, ex: number): Promise<any>

  persist(key: string): Promise<any>

  ttl(key: string): Promise<any>
}

interface RedisStringMethod {
  get(key: string): Promise<any>

  set(key: string, value: string | number, ex?: number, opt?: Options): Promise<any>
}

interface RedisHashMethod {
  hGet(key: string, field: string): Promise<any>

  hSet(key: string, field: string, value: string | number): Promise<any>

  hGetAll(key: string): Promise<any>

  hSetNX(key: string, field: string, value: string | number): Promise<any>

  hDel(key: string, field: string): Promise<any>

  hExists(key: string, field: string): Promise<any>

  hKeys(key: string): Promise<any>

  hVals(key: string): Promise<any>
}

interface RedisSetMethod {
  sAdd(key: string, value: string | number): Promise<any>

  sMembers(key: string): Promise<any>
}

interface RedisExtraMethod {
  autoGet (key: string): Promise<any>

  autoMGet (...keys: string[]): Promise<any>

  autoGetAll (): Promise<any>
}

const defaultRedisConnectionConfig: RedisConnectionConfig = {
  host: 'localhost',
  port: 6379,
  database: 0
}

export class RedisConnector implements RedisBaseMethod, RedisKeyMethod, RedisStringMethod, RedisHashMethod, RedisSetMethod, RedisExtraMethod {
  private client!: RedisClientType<any>
  public label!: string

  static async getInstance (config?: RedisConnectionConfig, label?: string) {
    if (config === undefined) {
      config = defaultRedisConnectionConfig
    }
    const instance = Object.create(RedisConnector.prototype)
    if (label === undefined) {
      instance.label = `redis_${config.host}:${config.port}/${config.database}_${config.user}`
    } else {
      instance.label = label
    }
    try {
      instance.client = await createClient({ url: toRedisConnectUrl(config) })
        .connect()
    } catch (e) {
      console.log(e)
      return null
    }
    return instance
  }

  public async close () {
    await this.client.disconnect()
  }

  // RedisBaseMethod
  public async ping () {
    return await this.client.ping()
  }

  public async select (db: number) {
    return await this.client.select(db)
  }

  public async dbSize () {
    return await this.client.dbSize()
  }

  public async flushDb () {
    return await this.client.flushDb()
  }

  public async flushAll () {
    return await this.client.flushAll()
  }

  // RedisKeyMethod
  public async del (...keys: string[]) {
    return await this.client.del(keys)
  }

  public async exists (key: string) {
    return await this.client.exists(key)
  }

  public async expire (key: string, ex: number) {
    return await this.client.expire(key, ex)
  }

  public async keys (pattern: string) {
    return await this.client.keys(pattern)
  }

  public async persist (key: string) {
    return await this.client.persist(key)
  }

  public async ttl (key: string) {
    return await this.client.ttl(key)
  }

  public async type (key: string) {
    return await this.client.type(key)
  }

  // RedisStringMethod
  public async get (key: string) {
    return await this.client.get(key)
  }

  public async set (key: string, value: string | number, ex?: number, opt?: Options) {
    const RedisQueryOptions: AttributeAddableObject = {}
    if (ex !== undefined) {
      RedisQueryOptions.EX = ex
    }
    if (opt !== undefined) {
      switch (opt) {
        case 'NX':
          RedisQueryOptions.NX = true
          break
        case 'XX':
          RedisQueryOptions.XX = true
          break
      }
    }
    return await this.client.set(key, value, RedisQueryOptions)
  }

  // RedisHashMethod
  public async hDel (key: string, field: string) {
    return await this.client.hDel(key, field)
  }

  public async hExists (key: string, field: string) {
    return await this.client.hExists(key, field)
  }

  public async hGet (key: string, field: string) {
    return await this.client.hGet(key, field)
  }

  public async hGetAll (key: string) {
    return await this.client.hGetAll(key)
  }

  public async hKeys (key: string) {
    return await this.client.hKeys(key)
  }

  public async hSet (key: string, field: string, value: string | number) {
    return await this.client.hSet(key, field, value)
  }

  public async hSetNX (key: string, field: string, value: string | number) {
    if (typeof value === 'number') {
      value = value.toString()
    }
    return await this.client.hSetNX(key, field, value)
  }

  public async hVals (key: string): Promise<any> {
    return await this.client.hVals(key)
  }

  // RedisSetMethod
  public async sAdd (key: string, value: string | number) {
    if (typeof value === 'number') {
      value = value.toString()
    }
    return await this.client.sAdd(key, value)
  }

  public async sMembers (key: string) {
    return await this.client.sMembers(key)
  }

  public async autoGet (key: string) {
    const type = await this.type(key)
    const pair: KeyValuePair = { key: key, type: type as Types, value: undefined, ttl: -2 }
    switch (type) {
      case 'string':
        pair.value = await this.get(key)
        break
      case 'hash':
        pair.value = JSON.stringify(await this.hGetAll(key))
        break
      case 'set':
        pair.value = await this.sMembers(key)
        break
      default:
        pair.value = '(unknown)'
        break
    }
    pair.ttl = await this.ttl(key)
    return pair
  }

  public async autoMGet (...keys: string[]) {
    const pairs: KeyValuePair[] = []
    for (const key of keys) {
      pairs.push(await this.autoGet(key))
    }
    return pairs
  }

  public async autoGetAll (): Promise<KeyValuePair[]> {
    const keys = await this.keys('*')
    return await this.autoMGet(...keys)
  }
}
