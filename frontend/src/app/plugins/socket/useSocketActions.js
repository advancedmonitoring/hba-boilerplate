import { mapActions } from 'pinia'

import { useAlertsStore } from '@/entities/alerts'
import { useUiStore } from '@/entities/ui'
import { useUserStore } from '@/entities/user'

import { useSocketStore } from '@/shared/socket'
import { getSocketNames } from '@/shared/utils/helpers'

const stores = [useSocketStore, useUiStore, useUserStore, useAlertsStore]

export default function* iterSocketActions(name) {
  for (const store of stores) {
    const actions = mapActions(store, getSocketNames(store()))
    if (actions.hasOwnProperty(name)) {
      yield actions
    }
  }
}
