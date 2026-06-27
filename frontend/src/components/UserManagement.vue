<template>
  <div class="container mt-4">
    <h2 class="mb-4">User List</h2>

    <div class="table-responsive">
      <table class="table table-dark table-striped table-hover align-middle">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in userList" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.phone }}</td>
            <td>
              <span class="badge" :class="user.is_blacklisted ? 'bg-danger' : 'bg-success'">
                {{ user.is_blacklisted ? 'Blacklisted' : 'Active' }}
              </span>
            </td>
            <td>
              <button class="btn btn-sm" :class="user.is_blacklisted ? 'btn-outline-success' : 'btn-outline-danger'" @click="toggleBlacklist(user.id)">
                {{ user.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
  </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'UserManagement',

    data() {
        return {
            userList: []
        }
    },

    async mounted() {
            try {
                const token = localStorage.getItem('token')
            
                const userResponse = await axios.get(
                    'http://localhost:5000/api/admin/users',
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                
                this.userList = userResponse.data
                
            } catch (error) {
                console.error(error)
            }
        },

    methods: {
                async toggleBlacklist(userId) {

            try {
            
                const token = localStorage.getItem('token')
            
                const response = await axios.put(
                    `http://localhost:5000/api/admin/toggle-blacklist/${userId}`,
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                
                alert(response.data.message)
                
                window.location.reload()
                
            } catch (error) {
            
                alert(
                    error.response?.data?.message ||
                    'Failed to update blacklist status'
                )
            
            }
        }
    }
}
</script>