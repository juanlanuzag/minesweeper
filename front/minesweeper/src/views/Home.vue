<template>
  <div class="home">
    {{info}}
  </div>
</template>

<script>
import axios from 'axios';


export default {
  name: 'Home',
  components: {
  },
  data () {
    return {
      info: null
    }
  },
  mounted () {
    axios
      .get('http://localhost:8000/api/minesweeper/')
      .then(response => (this.info = response))
  }
}
</script>
