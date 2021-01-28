<template>
  <div class="container" v-if="game">
    <div class="row">
      <div class="col"> Rows: {{game.rows}} </div>
      <div class="col"> Columns: {{game.columns}} </div>
      <div class="col"> Mines: {{game.mines}} </div>
    </div>
    <div v-if="game_status" class="row justify-content-end my-3">
      <div class="col-4"> <h3>{{game_status}}</h3> </div>
      <div class="col-4">
        <button type="button" class="btn btn-primary" @click="new_game">New Game</button>
      </div>
    </div>
    <div class="row">
      <div class="col board">
        <div class="board-col" v-for="(column, col_index) in board_to_display" :key="`col-${col_index}`">
          <div class="board-cell" v-for="(cell, row_index) in column"
               :key="`row-${col_index}-${row_index}`" @click.left="reveal_cell(col_index, row_index)"
               @click.right="flag_cell(col_index, row_index, $event)"
          >
            {{cell}}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import MinesweeperClient from "../api/MinesweeperClient";
import router from "../router";


export default {
  name: 'Home',
  props: ['id'],
  data () {
    return {
      game: null
    }
  },
  mounted () {
    this.loadGame();
  },
  methods: {
    loadGame() {
          MinesweeperClient.retrieve(this.$route.params.id)
                     .then(game => this.game = game);
    },
    cell_display_text(cell) {
      if (cell === 'hidden') return '';
      if (cell === 'mine') return 'M';
      if (cell === 'flag') return 'F';
      return cell;
    },
    reveal_cell(x_position, y_position) {
      MinesweeperClient.reveal_cell(this.$route.params.id, x_position, y_position)
                       .then(game => (this.game = game))
    },
    flag_cell(x_position, y_position, event) {
      if (event) {
        event.preventDefault()
      }
      const is_flagged = true;
      MinesweeperClient.flag_cell(this.$route.params.id, x_position, y_position, is_flagged)
                       .then(game => (this.game = game));
    },
    new_game() {
      MinesweeperClient.new_game(this.game.rows, this.game.columns, this.game.mines)
                       .then(game => {
                         router.push(`/game/${game.id}`);
      })
    },
  },
  computed: {
    game_status() {
      if (this.game && this.game.was_won) return "You WIN";
      if (this.game && this.game.was_lost) return "You LOST";
      return ""
    },
    board_to_display() {
      if (!this.game) return null;
      return this.game.board.map(row => row.map(this.cell_display_text))
    }
  },
  watch: {
      '$route': 'loadGame'
  }
}
</script>
<style>
  .board {
    display: flex;
    justify-content: center;
  }
  .board-cell {
    border: 1px solid black;
    height: 20px;
    width: 20px;
  }
</style>
