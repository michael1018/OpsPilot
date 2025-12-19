import axios from 'axios'

// Base URL，可根據後端修改
const BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:7000/api'

/**
 * Fetch users with pagination
 * @param {Number} pageindex
 * @param {Number} pagesize
 */
export async function getUsersPages(pageindex = 0, pagesize = 10) {
  const response = await axios.get(`${BASE_URL}/users_pages`, {
    params: { pageindex, pagesize }
  })
  return response.data
}

/**
 * Add a new user
 * @param {Object} user
 */
export async function createUser(user) {
  const response = await axios.post(`${BASE_URL}/users_create`, user)
  return response.data
}

/**
 * Update an existing user
 * @param {Object} user - Must include id
 */
export async function updateUser(user) {
  if (!user.id) throw new Error("Missing user id")
  const response = await axios.put(`${BASE_URL}/users_update`, user)
  return response.data
}

/**
 * Delete a user
 * @param {Number} id
 */
export async function deleteUser(id) {
  if (!id) throw new Error("Missing user id")
  // Axios delete 需要把 data 放在 config 裡
  const response = await axios.delete(`${BASE_URL}/users_delete`, {
    data: { id }
  })
  return response.data
}
