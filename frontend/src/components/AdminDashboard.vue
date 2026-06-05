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
            }
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

        }

    }
}

</script>