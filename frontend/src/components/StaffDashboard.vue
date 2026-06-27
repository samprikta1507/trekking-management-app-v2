<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4 border-bottom border-secondary pb-3">
      <h2>Staff Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <h4 class="mb-4">My Assigned Treks</h4>

    <div class="row g-4">
      <div class="col-lg-6" v-for="trek in treks" :key="trek.id">
        <div class="card text-bg-dark border-secondary shadow-sm h-100">
          <div class="card-body">
            
            <div class="d-flex justify-content-between align-items-start mb-3">
              <h5 class="card-title text-info fw-bold mb-0">{{ trek.trek_name }}</h5>
              <span class="badge" :class="trek.status === 'Completed' ? 'bg-primary' : (trek.status === 'Open' ? 'bg-success' : 'bg-warning text-dark')">
                {{ trek.status }}
              </span>
            </div>

            <div class="row mb-3 small">
              <div class="col-6 mb-2"><strong>Location:</strong> <br>{{ trek.location }}</div>
              <div class="col-6 mb-2"><strong>Difficulty:</strong> <br>{{ trek.difficulty }}</div>
              <div class="col-6"><strong>Slots Left:</strong> <br>{{ trek.available_slots }}</div>
              <div class="col-6"><strong>Trekkers:</strong> <br>{{ trek.registered_trekkers }}</div>
            </div>

            <div class="p-3 bg-secondary bg-opacity-10 rounded border border-secondary mb-4">
              <label class="form-label small text-secondary mb-2">Update Trek Status</label>
              <div class="input-group input-group-sm">
                <select v-model="trek.status" class="form-select text-bg-dark border-secondary">
                  <option>Open</option>
                  <option>Closed</option>
                  <option>Started</option>
                  <option>Completed</option>
                </select>
                <button class="btn btn-success px-3" @click="updateStatus(trek)">Update</button>
              </div>
            </div>

            <button class="btn w-100" :class="trek.showParticipants ? 'btn-secondary' : 'btn-outline-info'" @click="toggleParticipants(trek)">
              {{ trek.showParticipants ? 'Hide Participants' : 'View Participants' }}
            </button>

            <div v-if="trek.showParticipants" class="mt-3 slide-down">
              <h6 class="border-bottom border-secondary pb-2 mb-2 text-light">Participant List</h6>
              
              <div v-if="trek.participants && trek.participants.length > 0" class="table-responsive">
                <table class="table table-sm table-dark table-striped align-middle border-secondary mb-0">
                  <thead>
                    <tr>
                      <th class="text-secondary fw-normal">Name</th>
                      <th class="text-secondary fw-normal">Email</th>
                      <th class="text-secondary fw-normal text-end">Payment</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="participant in trek.participants" :key="participant.booking_id">
                      <td>{{ participant.user_name }}</td>
                      <td>{{ participant.email }}</td>
                      <td class="text-end">
                        <span class="badge" :class="participant.payment_status === 'Paid' ? 'bg-success' : 'bg-warning text-dark'">
                          {{ participant.payment_status }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-muted small fst-italic py-2 text-center border border-secondary rounded">
                No participants registered yet.
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import axios from "axios"

export default {

    name: "StaffDashboard",

    data() {
        return {
            treks: []
        }
    },

    async mounted() {

        try {

            const token = localStorage.getItem("token")

            const response = await axios.get(
                "http://127.0.0.1:5000/api/staff/my-treks",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            )

            this.treks = response.data

            this.treks.forEach(trek => {
                trek.participants = []
                trek.showParticipants = false
            })

        }
        catch (error) {

            console.error(error)

        }

    },

    methods: {

        async updateStatus(trek) {
        
            try {
            
                const token = localStorage.getItem("token")
            
                await axios.put(
                    `http://127.0.0.1:5000/api/staff/update-status/${trek.id}`,
                    {
                        status: trek.status
                    },
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                  
                alert("Status updated successfully")
                  
            }
            catch (error) {
            
                console.error(error)
            
            }
          
        },

        async loadParticipants(trek) {

          try {
          
              const token = localStorage.getItem("token")
          
              const response = await axios.get(
                  `http://127.0.0.1:5000/api/staff/participants/${trek.id}`,
                  {
                      headers: {
                          Authorization: `Bearer ${token}`
                      }
                  }
              )
                
              trek.participants = response.data
                
          }
          catch (error) {
          
              console.error(error)
          
          }
        
        },

        async toggleParticipants(trek) {

            if (trek.showParticipants) {
            
                trek.showParticipants = false
                return
            
            }
          
            if (trek.participants.length === 0) {
            
                await this.loadParticipants(trek)
            
            }
          
            trek.showParticipants = true
          
        },

        logout() {

            localStorage.removeItem("token")
            localStorage.removeItem("role")

            this.$router.push("/login")

        },
      
    }

}
</script>