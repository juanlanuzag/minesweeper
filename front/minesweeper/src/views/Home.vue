<template>
  <div class="container">
    <ul class="list-group" v-if="games">
      <li class="list-group-item" v-for="game in games" :key="game.id">
        <router-link :to="`/game/${game.id}`">Game {{game.id}}</router-link>
      </li>
    </ul>
    <button type="button"
            class="btn btn-primary"
            @click="new_game">New Game</button>
  </div>
</template>

<script>
import axios from 'axios';
import router from "../router";


export default {
  name: 'Home',
  components: {
  },
  data () {
    return {
      games: null
    }
  },
  methods: {
    new_game() {
      axios
      .post(`http://localhost:8000/api/minesweeper/`,
              {rows: 5, columns: 5, mines: 5})
      .then(response => {
          let id = response.data.id;
          router.push(`/game/${id}`)
      })
    },
  },
  mounted () {
    axios
      .get('http://localhost:8000/api/minesweeper/')
      .then(response => (this.games = response.data))
  }
}
</script>
