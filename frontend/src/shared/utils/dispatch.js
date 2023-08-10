const _stores = {}

export const dispatchPlugin = ({ store }) => {
  _stores[store.$id] = store
}

export const dispatch = (moduleName, actionName, ...data) => {
  return _stores[moduleName][actionName](...data)
}

export const get = (moduleName, getterName) => {
  return _stores[moduleName][getterName]
}
