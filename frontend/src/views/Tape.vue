<template>
  <div>
      <h1>Header</h1>
  </div>
</template>

<script>
export default {
  name: 'Tape',
  data () {
    return {
      url: `${window.location.protocol}//${window.location.hostname}:5000/login`
    }
  },
  methods: {
  }
}
</script>
