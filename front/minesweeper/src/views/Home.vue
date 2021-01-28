<template>
  <div class="container">
    <div class="row my-4">
      <div class="col">
        <div class="form-group">
          <label for="rows">Rows</label>
          <input id="rows" v-model="rows" type="number" min="1" class="form-control">
        </div>
      </div>
      <div class="col">
        <div class="form-group">
          <label for="columns">Columns</label>
          <input id="columns" v-model="columns" type="number" min="1" class="form-control">
        </div>
      </div>
      <div class="col">
        <div class="form-group">
          <label for="mines">Mines</label>
          <input id="mines" v-model="mines" type="number" min="1" class="form-control">
        </div>
      </div>
      <div class="col">
        <button type="button"
            class="btn btn-primary mt-4"
            @click="new_game">New Game</button>
      </div>
    </div>
    <ul class="list-group" v-if="games">
      <li class="list-group-item" v-for="game in games" :key="game.id">
        <router-link :to="`/game/${game.id}`">Game {{game.id}}</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import router from "../router";
import MinesweeperClient from "../api/MinesweeperClient";


export default {
  name: 'Home',
  components: {
  },
  data () {
    return {
      games: null,
      rows: 5,
      columns: 5,
      mines: 5
    }
  },
  methods: {
    new_game() {
      MinesweeperClient.new_game(this.rows, this.columns, this.mines)
                       .then(game => { router.push(`/game/${game.id}`);
      })
    },
  },
  mounted () {
    MinesweeperClient.list().then(games => (this.games = games));
  }
}
</script>
