import i18n from '@/shared/translation'

class User {
  constructor(obj) {
    this.id = obj.id
    this.username = obj.username
    this.firstName = obj.firstName || ''
    this.lastName = obj.lastName || ''
    this.email = obj.email || ''
    this.isOnline = obj.isOnline
  }

  get fullName() {
    return `${this.lastName} ${this.firstName}`.trim()
  }

  get initials() {
    const firstName = this.firstName ? this.firstName[0] : '-'
    const lastName = this.lastName ? this.lastName[0] : '-'
    return `${lastName}${firstName}`
  }
}

export default User

export class AnonymousUser extends User {
  constructor(name) {
    super({ id: null, username: name || i18n.global.t('main.hiddenUser') })
  }
}
