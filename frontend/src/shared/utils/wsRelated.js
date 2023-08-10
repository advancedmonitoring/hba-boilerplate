const getSetDef = (store, valueKey) => {
  return (data) => {
    store[valueKey] = data[valueKey]
  }
}

const getAddedDef = (store, valueKey) => {
  return (data) => {
    const index = store[valueKey].findIndex((item) => item.id === data.id)
    if (index === -1) {
      store[valueKey].push(data)
    }
  }
}

const getUpdatedDef = (store, valueKey) => {
  return (data) => {
    const items = store[valueKey]
    const index = items.findIndex((item) => data.id === item.id)
    if (index !== -1) {
      const stored = items[index]
      items[index] = { ...stored, ...data }
    }
  }
}

const getDeletedDef = (store, itemKey, valueKey) => {
  return (data) => {
    const id = data[`${itemKey}Id`]
    store[valueKey] = store[valueKey].filter((item) => item.id !== id)
  }
}

export const wsRelatedPlugin = ({ options, store }) => {
  if (options.wsRelated) {
    return Object.keys(options.wsRelated).reduce((wsActions, itemKey) => {
      const valueKey = options.wsRelated[itemKey]
      wsActions[`SOCKET_${valueKey}`] = getSetDef(store, valueKey)
      wsActions[`SOCKET_${itemKey}_added`] = getAddedDef(store, valueKey)
      wsActions[`SOCKET_${itemKey}_updated`] = getUpdatedDef(store, valueKey)
      wsActions[`SOCKET_${itemKey}_deleted`] = getDeletedDef(store, itemKey, valueKey)

      return wsActions
    }, {})
  }
}
