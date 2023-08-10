import { required } from '@vee-validate/rules'
import { defineRule, configure } from 'vee-validate'

import i18n from '@/shared/translation'

defineRule('required', required)

configure({
  generateMessage: (context) => {
    return i18n.global.t(`validate.rules.${context.rule.name}`, context.rule.params)
  },
})
