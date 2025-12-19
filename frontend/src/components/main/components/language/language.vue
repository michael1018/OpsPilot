<template>
  <div>
    <Dropdown trigger="click" @on-click="selectLang">
      <a href="javascript:void(0)">
        {{ title }}
        <Icon :size="18" type="md-arrow-dropdown" />
      </a>
      <DropdownMenu slot="list">
        <DropdownItem v-for="(value, key) in localList" :name="key" :key="`lang-${key}`">{{ value }}</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  </div>
</template>

<script>
export default {
  name: 'Language',
  props: {
    lang: String
  },
  data () {
    return {
      langList: {
        'zh_CN': '语言',
        'zh_TW': '語言',
        'en_US': 'Lang',
        'ja_JP': '言語',
        'hi_IN': 'bahasa',
        'in_ID': 'भाषा: हिन्दी',
        'th_TH': 'ภาษา',
        'ko_KR': '언어',
        'vi_VN': 'ngôn ngữ'
      },
      localList: {
        'zh_CN': '中文简体',
        'zh_TW': '中文繁体',
        'en_US': 'English',
        'ja_JP': '日本語',
        'hi_IN': 'bahasa Indonesia',
        'in_ID': 'हिंदी',
        'th_TH': 'ไทย',
        'ko_KR': '한국어',
        'vi_VN': 'Tiếng Việt'
      }
    }
  },
  watch: {
    lang (lang) {
      this.$i18n.locale = lang
    }
  },
  computed: {
    title () {
      return this.langList[this.lang]
    }
  },
  methods: {
    selectLang (name) {
      this.$emit('on-lang-change', name)
    }
  }
}
</script>
