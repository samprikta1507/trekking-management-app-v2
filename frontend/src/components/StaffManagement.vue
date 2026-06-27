<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Staff Management</h2>
      <button class="btn btn-primary" @click="showStaffForm = !showStaffForm">
        {{ showStaffForm ? 'Close Form' : 'Add New Staff' }}
      </button>
    </div>

    <div v-if="showStaffForm" class="card text-bg-dark border-secondary mb-4">
      <div class="card-body">
        <h5 class="card-title mb-4 border-bottom border-secondary pb-2">
          {{ editingStaffId ? 'Update Staff Member' : 'Create Staff Member' }}
        </h5>
        
        <form @submit.prevent="saveStaff">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Name</label>
              <input type="text" class="form-control text-bg-dark" v-model="staffForm.name" required>
            </div>
            <div class="col-md-6">
              <label class="form-label">Email</label>
              <input type="email" class="form-control text-bg-dark" v-model="staffForm.email" required>
            </div>
            <div class="col-md-6">
              <label class="form-label">Phone</label>
              <input type="text" class="form-control text-bg-dark" v-model="staffForm.phone" required>
            </div>
            <div class="col-md-6">
              <label class="form-label">Password</label>
              <input type="password" class="form-control text-bg-dark" v-model="staffForm.password" :required="!editingStaffId">
            </div>
            <div class="col-md-6">
              <label class="form-label">Experience (Years)</label>
              <input type="number" class="form-control text-bg-dark" v-model="staffForm.experience_years" required>
            </div>
            <div class="col-md-6">
              <label class="form-label">Specialization</label>
              <input type="text" class="form-control text-bg-dark" v-model="staffForm.specialization" required>
            </div>
          </div>
          <div class="mt-4 text-end">
            <button type="submit" class="btn btn-success px-4">
              {{ editingStaffId ? 'Save Changes' : 'Create Staff' }}
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
            <th>Email</th>
            <th>Phone</th>
            <th>Specialization</th>
            <th class="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="staff in staffList" :key="staff.id">
            <td>{{ staff.name }}</td>
            <td>{{ staff.email }}</td>
            <td>{{ staff.phone }}</td>
            <td>{{ staff.specialization || 'General' }}</td>
            <td class="text-end">
              <button class="btn btn-sm btn-outline-info me-2" @click="editStaff(staff)">Edit</button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteStaff(staff.id)">Delete</button>
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
    name: 'StaffManagement',
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
            
            console.log("STAFF API RESPONSE:", response.data)
            
            this.staffList = response.data
            
        } catch (error) {
            console.error("STAFF LOAD ERROR:", error)
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
    }
}
</script>