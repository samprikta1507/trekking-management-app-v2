<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Trek Management</h2>
      <button class="btn btn-primary" @click="showTrekForm = !showTrekForm">
        {{ showTrekForm ? 'Close Form' : 'Add New Trek' }}
      </button>
    </div>

    <div v-if="showTrekForm" class="card text-bg-dark border-secondary mb-4">
      <div class="card-body">
        <h5 class="card-title mb-4 border-bottom border-secondary pb-2">
          {{ isEditingTrek ? 'Update Trek' : 'Create Trek' }}
        </h5>
        
        <form @submit.prevent="saveTrek">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Trek Name</label>
              <input type="text" class="form-control text-bg-dark" v-model="trekForm.trek_name" required>
            </div>
            <div class="col-md-6">
              <label class="form-label">Location</label>
              <input type="text" class="form-control text-bg-dark" v-model="trekForm.location" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">Difficulty</label>
              <input type="text" class="form-control text-bg-dark" v-model="trekForm.difficulty" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">Duration (Days)</label>
              <input type="number" class="form-control text-bg-dark" v-model="trekForm.duration_days" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">Available Slots</label>
              <input type="number" class="form-control text-bg-dark" v-model="trekForm.available_slots" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">Assigned Staff ID</label>
              <input type="number" class="form-control text-bg-dark" v-model="trekForm.assigned_staff_id" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">Start Date</label>
              <input type="date" class="form-control text-bg-dark" v-model="trekForm.start_date" required>
            </div>
            <div class="col-md-4">
              <label class="form-label">Price (₹)</label>
              <input type="number" class="form-control text-bg-dark" v-model="trekForm.price" required>
            </div>
          </div>
          <div class="mt-4 text-end">
            <button type="submit" class="btn btn-success px-4">
              {{ isEditingTrek ? 'Save Changes' : 'Create Trek' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div class="table-responsive">
      <table class="table table-dark table-striped table-hover align-middle border-secondary">
        <thead>
          <tr>
            <th>Name</th>
            <th>Location</th>
            <th>Difficulty</th>
            <th>Duration</th>
            <th>Slots</th>
            <th>Price</th>
            <th>Status</th>
            <th class="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="trek in trekList" :key="trek.id">
            <td class="fw-bold">{{ trek.trek_name }}</td>
            <td>{{ trek.location }}</td>
            <td>{{ trek.difficulty }}</td>
            <td>{{ trek.duration_days }} days</td>
            <td>{{ trek.available_slots }}</td>
            <td>₹{{ trek.price }}</td>
            <td>
              <span class="badge" :class="trek.status === 'Pending' ? 'bg-warning text-dark' : 'bg-success'">
                {{ trek.status }}
              </span>
            </td>
            <td class="text-end">
              <button class="btn btn-sm btn-outline-info me-2" @click="editTrek(trek)">Edit</button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteTrek(trek.id)">Delete</button>
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
    name: 'TrekManagement',

    data() {
        return {
            trekList: [],

            showTrekForm: false,
                    
            isEditingTrek: false,
                    
            editingTrekId: null,
                    
            trekForm: {
                trek_name: '',
                location: '',
                difficulty: '',
                duration_days: '',
                available_slots: '',
                assigned_staff_id: '',
                start_date: '',
                end_date: '',
                price: '',
                status: 'Pending'
            },
        }
    },

    async mounted() {
        try {
            const token = localStorage.getItem('token')
        
            const trekResponse = await axios.get(
                'http://localhost:5000/api/admin/treks',
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            )
            
            this.trekList = trekResponse.data
            
        } catch (error) {
            console.error(error)
        }
    },

    methods: {
                async createTrek() {

            try {
            
                const token = localStorage.getItem('token')
            
                const response = await axios.post(
                    'http://localhost:5000/api/admin/create-trek',
                    this.trekForm,
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
                    'Failed to create trek'
                )
            
            }
        
        },

        async saveTrek() {

            if (this.isEditingTrek) {
            
                this.updateTrek()
            
            } else {
            
                this.createTrek()
            
            }
        
        },

        async deleteTrek(trekId) {

            try {
            
                const token = localStorage.getItem('token')
            
                const response = await axios.delete(
                    `http://localhost:5000/api/admin/delete-trek/${trekId}`,
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
                    'Failed to delete trek'
                )
            
            }
        
        },

        async updateTrek() {
                
            try {
            
                const token = localStorage.getItem('token')
            
                const response = await axios.put(
                    `http://localhost:5000/api/admin/update-trek/${this.editingTrekId}`,
                    this.trekForm,
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
                    'Failed to update trek'
                )
            
            }
        
        },

        editTrek(trek) {

            this.showTrekForm = true

            this.isEditingTrek = true

            this.editingTrekId = trek.id

            this.trekForm.trek_name = trek.trek_name
            this.trekForm.location = trek.location
            this.trekForm.difficulty = trek.difficulty
            this.trekForm.duration_days = trek.duration_days
            this.trekForm.available_slots = trek.available_slots
            this.trekForm.assigned_staff_id = trek.assigned_staff_id
            this.trekForm.start_date = trek.start_date
            this.trekForm.end_date = trek.end_date
            this.trekForm.price = trek.price
            this.trekForm.status = trek.status

        },
    }
}
</script>