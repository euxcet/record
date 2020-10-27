<template>
    <div class="main" @contextmenu.prevent="">
      <div v-html="title" class="record-title"></div>
      <div v-html="message" class="record-message"></div>
      <!--span class="record-remain">{{count}}</span-->
      <div class="record-row">
        <el-button class="record-button" size="small" type="primary" @click="getTask">{{button}}</el-button>
      </div>
      <img class="cross" :src="cross" :height=cross_height :style="{'top':position.y,'left':position.x}">
    </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'Record',
  data () {
    return {
      begin_url: `${window.location.protocol}//${window.location.hostname}:5000/begin`,
      end_url: `${window.location.protocol}//${window.location.hostname}:5000/end`,
      button: '录制',
      title: '',
      message: '',
      query: {
        'stage': 0,
        'task': 0,
        'count': 1,
        'first': 1
      },
      count: '',
      cross_height: 150,
      totalTime: 30,
      position: {
        'x': '-200px',
        'y': '-200px'
      },
      cross: require('../assets/image/cross.jpg')
    }
  },
  mounted () {
    if (typeof this.$route.query.stage === 'undefined') {
      this.query.stage = 0
      this.query.task = 0
      this.query.count = 1
      this.query.first = 1
    } else {
      this.query.stage = this.$route.query.stage
      this.query.task = this.$route.query.task
      this.query.count = 0
      this.query.first = 1
    }
  },
  methods: {
    getTask () {
      if (this.button === '开始') {
        axios.post(this.begin_url, this.query, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }).then(response => {
          this.totalTime = response.data.time
          this.button = this.totalTime + 's'
          let clock = window.setInterval(() => {
            this.totalTime--
            this.button = this.totalTime + 's'
            if (this.totalTime < 0) {
              window.clearInterval(clock)
              this.totalTime = 30
              this.button = '结束'
            }
          }, 1000)
        })
      } else if (this.button === '结束' || this.button === '录制') {
        axios.post(this.end_url, this.query, {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }).then(response => {
          if (response.data.hascross) {
            this.cross_height = 150
          } else {
            this.cross_height = 0
          }
          this.query.stage = response.data.stage
          this.query.task = response.data.task
          this.query.count = response.data.count
          this.query.first = 1
          this.count = '剩余次数：' + response.data.remain.toString()
          this.title = response.data.title
          this.message = response.data.message
          this.position.x = response.data.x.toString() + 'px'
          this.position.y = response.data.y.toString() + 'px'
          this.button = '开始'
        })
      }
    }
  }
}
</script>
