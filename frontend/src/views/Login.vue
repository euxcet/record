<template>
  <div class="main">
    <h1>{{title}}</h1>
    <div class="login-form-container">
      <el-form :model="login">
        <div class="login-form-row">
          <label class="login-form-label">姓名</label>
          <el-input class="login-form-input" placeholder clearable v-model.trim="login.name"></el-input>
        </div>
        <div class="login-form-row">
          <label class="login-form-label">学号</label>
          <el-input class="login-form-input" placeholder clearable v-model.trim="login.sid"></el-input>
        </div>
        <div class="login-form-row">
          <label class="login-form-label">年龄</label>
          <el-input-number class="login-number" v-model="login.age" :min=18 :max=50 :step=1 label="年龄"></el-input-number>
        </div>
        <div class="login-form-row">
          <label class="login-form-label">惯用手</label>
          <el-radio class="login-radio" v-model="login.is_right" label=true>右手</el-radio>
          <el-radio class="login-radio" v-model="login.is_right" label=false>左手</el-radio>
        </div>
        <div class="login-form-row">
          <label class="login-form-label">手机材质</label>
          <el-radio class="login-radio" v-model="login.is_metal" label=true>金属</el-radio>
          <el-radio class="login-radio" v-model="login.is_metal" label=false>塑料</el-radio>
        </div>
        <div class="login-form-row">
          <label class="login-form-label">手机是否有壳</label>
          <el-radio class="login-radio" v-model="login.has_case" label=true>有</el-radio>
          <el-radio class="login-radio" v-model="login.has_case" label=false>无</el-radio>
        </div>
        <div class="login-form-row">
          <el-button class="login-form-button" size="small" type="primary" @click="submit">OK</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data () {
    return {
      title: '数据录入系统',
      url: 'http://127.0.0.1:5000/login',
      login: {
        name: '',
        sid: 0,
        age: 20,
        is_right: 'true',
        is_metal: 'true',
        has_case: 'true'
      }
    }
  },
  methods: {
    submit () {
      axios.post(this.url, this.login, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).then(response => (this.$router.push({name: 'Record'})))
    }
  }
}
</script>
