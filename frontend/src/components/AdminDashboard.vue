<template>
    <div>
        <h1>Admin Dashboard</h1>

        <button @click="showStaffForm = !showStaffForm">Add Staff</button>
        <div v-if="showStaffForm">

          <h3>Create Staff</h3>
              
          <form @submit.prevent="saveStaff">
          
              <div>
                  <label>Name:</label>
                  <input type="text" v-model="staffForm.name"required>
              </div>
            
              <div>
                  <label>Email:</label>
                  <input type="email" v-model="staffForm.email" required>
              </div>
            
              <div>
                  <label>Phone:</label>
                  <input type="text" v-model="staffForm.phone" required>
              </div>
            
              <div>
                  <label>Password:</label>
                  <input type="password" v-model="staffForm.password" required>
              </div>
            
              <div>
                  <label>Experience:</label>
                  <input type="number" v-model="staffForm.experience_years" required>
              </div>
            
              <div>
                  <label>Specialization:</label>
                  <input type="text" v-model="staffForm.specialization" required>
              </div>
            
              <button type="submit">{{ isEditing ? 'Update Staff' : 'Create Staff' }}</button>
          </form>
        
          <hr>
        
        </div>

        <h2>Staff List</h2>

        <div v-for="staff in staffList" :key="staff.id">

            <p>Name: {{ staff.name }}</p>
            <p>Email: {{ staff.email }}</p>
            <p>Phone: {{ staff.phone }}</p>

            <button @click="deleteStaff(staff.id)">Delete</button>
            <button @click="editStaff(staff)">Edit</button>

            <hr>

        </div>

        <h2>Trek Management</h2>

        <button @click="showTrekForm = !showTrekForm">Add Trek</button>
        <div v-if="showTrekForm">

            <h3>Create Trek</h3>

            <form @submit.prevent="saveTrek">

                <div>
                    <label>Trek Name:</label>
                    <input type="text" v-model="trekForm.trek_name">
                </div>

                <div>
                    <label>Location:</label>
                    <input type="text" v-model="trekForm.location">
                </div>

                <div>
                    <label>Difficulty:</label>
                    <input type="text" v-model="trekForm.difficulty">
                </div>

                <div>
                    <label>Duration Days:</label>
                    <input type="number" v-model="trekForm.duration_days">
                </div>

                <div>
                    <label>Available Slots:</label>
                    <input type="number" v-model="trekForm.available_slots">
                </div>

                <div>
                    <label>Assigned Staff ID:</label>
                    <input type="number" v-model="trekForm.assigned_staff_id">
                </div>

                <div>
                    <label>Start Date:</label>
                    <input type="date" v-model="trekForm.start_date">
                </div>

                <div>
                    <label>End Date:</label>
                    <input type="date" v-model="trekForm.end_date">
                </div>

                <div>
                    <label>Price:</label>
                    <input type="number" v-model="trekForm.price">
                </div>

                <button type="submit">{{ isEditingTrek ? 'Update Trek' : 'Create Trek' }}</button>

            </form>

        </div>

        <h3>Trek List</h3>

        <div v-for="trek in trekList" :key="trek.id">
        
            <p>Trek Name: {{ trek.trek_name }}</p>
        
            <p>Location: {{ trek.location }}</p>
        
            <p>Difficulty: {{ trek.difficulty }}</p>
        
            <p>Duration: {{ trek.duration_days }} days</p>
        
            <p>Available Slots: {{ trek.available_slots }}</p>
        
            <p>Status: {{ trek.status }}</p>
        
            <p>Price: ₹{{ trek.price }}</p>

            <button @click="editTrek(trek)">Edit</button>
            <button @click="deleteTrek(trek.id)">Delete</button>
        
            <hr>
        
        </div>

        <h2>User List</h2>

        <div v-for="user in userList" :key="user.id">
        
            <p>Name: {{ user.name }}</p>
        
            <p>Email: {{ user.email }}</p>
        
            <p>Blacklisted: {{ user.is_blacklisted }}</p>

            <button @click="toggleBlacklist(user.id)">{{ user.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}</button>
        
            <hr>
        
        </div>

    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'AdminDashboard',

    data() {
        return {
            staffList: [],

            showStaffForm: false,

            isEditing: false,

            editingStaffId: null,

            staffForm: {
                name: '',
                email: '',
                phone: '',
                password: '',
                experience_years: '',
                specialization: ''
            },
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
            userList: [],

        }
    },

    async mounted() {

        try {

            const token = localStorage.getItem('token')

            const response = await axios.get(
                'http://localhost:5000/api/admin/staff',
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            )

            this.staffList = response.data

            const trekResponse = await axios.get(
                'http://localhost:5000/api/admin/treks',
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            )

            this.trekList = trekResponse.data

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

        async createStaff() {

            try {

                const token = localStorage.getItem('token')

                const response = await axios.post(
                    'http://localhost:5000/api/admin/create-staff',
                    this.staffForm,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )

                alert(response.data.message)

                this.staffForm.name = ''
                this.staffForm.email = ''
                this.staffForm.phone = ''
                this.staffForm.password = ''
                this.staffForm.experience_years = ''
                this.staffForm.specialization = ''

                window.location.reload()

            } catch (error) {

                alert(
                    error.response?.data?.message ||
                    'Failed to create staff'
                )

            }

        },

        async saveStaff() {

          if (this.isEditing) {

              this.updateStaff()

          } else {

            this.createStaff()

          }

        },

        async deleteStaff(staffId) {
            try {
                const token = localStorage.getItem('token')

                const response = await axios.delete(
                    `http://localhost:5000/api/admin/delete-staff/${staffId}`,
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
                    'Failed to delete staff'
                )
            }
        },

        async updateStaff() {

          try {

            const token = localStorage.getItem('token')

            const response = await axios.put(
              `http://localhost:5000/api/admin/update-staff/${this.editingStaffId}`,
              this.staffForm,
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
              'Failed to update staff'
            )
          }
        },

        editStaff(staff) {

          this.showStaffForm = true

          this.isEditing = true

          this.editingStaffId = staff.id

          this.staffForm.name = staff.name
          this.staffForm.email = staff.email
          this.staffForm.phone = staff.phone
          this.staffForm.experience_years = staff.experience_years
          this.staffForm.specialization = staff.specialization

        },

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