import { type RedisConnectionConfig } from '@/scripts/RedisConnector'

export function toRedisConnectUrl (config: RedisConnectionConfig) {
    let formatUrl = 'redis://'
    if (config.user !== undefined) {
        formatUrl += `${config.user}`
        if (config.password !== undefined) {
            formatUrl += `:${config.password}`
        }
        formatUrl += '@'
    }
    if (config.host !== undefined) {
        formatUrl += `${config.host}`
    }
    if (config.port !== undefined) {
        formatUrl += `:${config.port}`
    }
    if (config.database !== undefined) {
        formatUrl += `/${config.database}`
    }
    return formatUrl
}
