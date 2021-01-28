import axios from "axios";

const base_url = 'http://localhost:8000/'
const api_url = `${base_url}api/minesweeper/`

export default {
    new_game(rows, columns, mines) {
      return axios.post(api_url, {rows, columns, mines})
                  .then(response => response.data);
    },
    list() {
      return axios.get(api_url)
                  .then(response => response.data)
    },
    retrieve(game_id) {
        return axios.get(`${api_url}${game_id}`)
                    .then(response => response.data);
    },
    reveal_cell(game_id, x_position, y_position) {
        return axios.post(`${api_url}${game_id}/reveal_cell/`, {x_position, y_position })
                    .then(response => response.data);
    },
    flag_cell(game_id, x_position, y_position, is_flagged) {
        return axios.post(`${api_url}${game_id}/flag_cell/`, {x_position, y_position, is_flagged })
                    .then(response => response.data);
    },
}
