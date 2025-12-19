<template>
  <Form ref="loginForm" :model="form" :rules="rules" @keydown.enter.native="handleSubmit">
    <FormItem :label="$t('login.account_type')" prop="type">
      <Select v-model="form.type">
        <Option value="master">{{$t('login.master')}}</Option>
        <Option value="child">{{$t('login.child')}}</Option>
      </Select>
    </FormItem>
    <FormItem prop="userName">
      <Input v-model="form.userName" :placeholder="$t('login.username_placeholder')">
        <span slot="prepend">
          <Icon :size="16" type="ios-person"></Icon>
        </span>
      </Input>
    </FormItem>
    <FormItem prop="password">
      <Input type="password" v-model="form.password" :placeholder="$t('login.password_placeholder')">
        <span slot="prepend">
          <Icon :size="14" type="md-lock"></Icon>
        </span>
      </Input>
    </FormItem>
    <FormItem prop="gac">
      <Input v-model="form.gac" :placeholder="$t('login.gac_placeholder')">
        <span slot="prepend">
          <Icon :size="14" type="md-lock"></Icon>
        </span>
      </Input>
    </FormItem>
    <FormItem>
      <Button @click="handleSubmit" type="primary" long>{{$t('login.login')}}</Button>
    </FormItem>
  </Form>
</template>
<script>
export default {
  name: 'LoginForm',
  props: {
    userNameRules: {
      type: Array,
      default: function () {
        return [
          { required: true, message: this.$t('error.username_is_empty'), trigger: 'blur' }
        ]
      }
    },
    passwordRules: {
      type: Array,
      default: function () {
        return [
          { required: true, message: this.$t('error.password_is_empty'), trigger: 'blur' }
        ]
      }
    },
    gacRules: {
      type: Array,
      default: function () {
        return [
          { required: true, message: this.$t('error.gac_is_empty'), trigger: 'blur' }
        ]
      }
    }
  },
  data () {
    return {
      form: {
        type: 'master',
        userName: '',
        password: '',
        gac: ''
      }
    }
  },
  computed: {
    rules () {
      return {
        userName: this.userNameRules,
        password: this.passwordRules,
        gac: this.gacRules
      }
    }
  },
  methods: {
    handleSubmit () {
      this.$refs.loginForm.validate((valid) => {
        if (valid === true) {
          this.$emit('on-success-valid', {
            userName: this.form.userName,
            password: this.form.password,
            isMaster: this.form.type === 'master',
            gac: this.form.gac
          })
        } else {
          console.error('handleSubmit validate 失敗', valid)
        }
      })
    }
  }
}
</script>
