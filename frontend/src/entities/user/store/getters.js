import User, { AnonymousUser } from '../models/user'

export const getters = {
  user(state) {
    return (state.userData && new User(state.userData)) || new AnonymousUser()
  },
}
