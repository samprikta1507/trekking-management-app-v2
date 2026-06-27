<template>
  <div class="container mt-4">
    
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2 class="mb-1">User Dashboard</h2>
        <p class="text-secondary mb-0">Welcome back, {{ email }}</p>
      </div>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <div class="d-flex justify-content-between mb-4 border-bottom border-secondary pb-3">
      <div class="btn-group" role="group">
        <button class="btn" :class="activeTab === 'treks' ? 'btn-primary' : 'btn-outline-secondary'" @click="activeTab = 'treks'">Available Treks</button>
        <button class="btn" :class="activeTab === 'bookings' ? 'btn-primary' : 'btn-outline-secondary'" @click="activeTab = 'bookings'">My Bookings</button>
        <button class="btn" :class="activeTab === 'profile' ? 'btn-primary' : 'btn-outline-secondary'" @click="activeTab = 'profile'">Profile</button>
      </div>
      
      <button @click="exportTrekHistory" :disabled="isExporting" class="btn btn-success shadow-sm">
        <span v-if="isExporting">
          <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
          Generating CSV...
        </span>
        <span v-else>
          <i class="bi bi-download me-2"></i>Export My Trek History
        </span>
      </button>
    </div>

    <div v-if="exportMessage" class="alert alert-info shadow-sm">
      {{ exportMessage }}
    </div>

    <div v-if="activeTab === 'treks'">
      
      <div class="card text-bg-dark border-secondary mb-4 shadow-sm">
        <div class="card-body">
          <h5 class="card-title mb-3">Find Your Next Adventure</h5>
          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label text-secondary small">Difficulty</label>
              <select v-model="selectedDifficulty" class="form-select text-bg-dark border-secondary">
                <option value="">All Levels</option>
                <option value="Easy">Easy</option>
                <option value="Moderate">Moderate</option>
                <option value="Hard">Hard</option>
              </select>
            </div>
            <div class="col-md-4">
              <label class="form-label text-secondary small">Location</label>
              <input type="text" v-model="selectedLocation" class="form-control text-bg-dark border-secondary" placeholder="Search location...">
            </div>
            <div class="col-md-4">
              <label class="form-label text-secondary small">Max Duration (Days)</label>
              <input type="number" v-model="selectedDuration" class="form-control text-bg-dark border-secondary" placeholder="e.g. 5">
            </div>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-md-6 col-lg-4" v-for="trek in filteredTreks" :key="trek.id">
          <div class="card h-100 text-bg-dark border-secondary shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h5 class="card-title text-info fw-bold mb-0">{{ trek.trek_name }}</h5>
                <span class="badge" :class="trek.difficulty === 'Easy' ? 'bg-success' : (trek.difficulty === 'Moderate' ? 'bg-warning text-dark' : 'bg-danger')">
                  {{ trek.difficulty }}
                </span>
              </div>
              <h6 class="card-subtitle mb-3 text-secondary"><i class="bi bi-geo-alt-fill me-1"></i>{{ trek.location }}</h6>
              
              <ul class="list-unstyled small mb-4">
                <li class="mb-1"><strong>Duration:</strong> {{ trek.duration_days }} Days</li>
                <li class="mb-1"><strong>Slots Available:</strong> <span :class="trek.available_slots > 0 ? 'text-success' : 'text-danger'">{{ trek.available_slots }}</span></li>
                <li class="fs-5 mt-2"><strong>₹{{ trek.price }}</strong></li>
              </ul>
            </div>
            <div class="card-footer bg-transparent border-top border-secondary">
              <button class="btn btn-primary w-100" @click="bookTrek(trek.id)" :disabled="trek.available_slots === 0">
                {{ trek.available_slots > 0 ? 'Book This Trek' : 'Sold Out' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'bookings'">
      <h4 class="mb-4">My Bookings</h4>
      <div class="row g-4">
        <div class="col-md-6" v-for="booking in bookings" :key="booking.booking_id">
          <div class="card text-bg-dark border-secondary shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="card-title text-info fw-bold mb-0">{{ booking.trek_name }}</h5>
                <span class="badge" :class="booking.status === 'Booked' ? 'bg-success' : (booking.status === 'Cancelled' ? 'bg-danger' : (booking.status === 'Completed' ? 'bg-primary' : 'bg-warning text-dark'))">
                  {{ booking.status }}
                </span>
              </div>
              
              <p class="text-secondary small mb-3"><i class="bi bi-geo-alt-fill me-1"></i>{{ booking.location }}</p>
              
              <div class="p-3 bg-secondary bg-opacity-10 rounded border border-secondary mb-3">
                <div class="row small">
                  <div class="col-6 mb-2"><strong>Start:</strong><br>{{ booking.start_date }}</div>
                  <div class="col-6 mb-2"><strong>End:</strong><br>{{ booking.end_date }}</div>
                  <div class="col-6"><strong>Payment:</strong><br>
                    <span :class="booking.payment_status === 'Paid' ? 'text-success' : 'text-warning'">{{ booking.payment_status }}</span>
                  </div>
                  <div class="col-6"><strong>Booked On:</strong><br>{{ booking.booking_date.split(' ')[0] }}</div>
                </div>
              </div>

              <div class="d-flex gap-2">
                <button v-if="booking.payment_status === 'Pending' && booking.status !== 'Cancelled'" class="btn btn-success flex-grow-1" @click="payBooking(booking.booking_id)">
                  Pay Now
                </button>
                <button v-if="booking.status === 'Booked'" class="btn btn-outline-danger flex-grow-1" @click="cancelBooking(booking.booking_id)">
                  Cancel Booking
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'profile'" class="row justify-content-center">
      <div class="col-md-6">
        <div class="card text-bg-dark border-secondary shadow-sm">
          <div class="card-body p-4">
            <h4 class="card-title mb-4 border-bottom border-secondary pb-2">Profile Settings</h4>
            
            <div class="mb-3">
              <label class="form-label text-secondary small">Name</label>
              <input type="text" v-model="profile.name" class="form-control text-bg-dark border-secondary">
            </div>
            
            <div class="mb-3">
              <label class="form-label text-secondary small">Email (Read Only)</label>
              <input type="email" v-model="profile.email" class="form-control text-bg-secondary border-secondary text-muted" readonly>
            </div>
            
            <div class="mb-4">
              <label class="form-label text-secondary small">Phone Number</label>
              <input type="text" v-model="profile.phone" class="form-control text-bg-dark border-secondary">
            </div>
            
            <button class="btn btn-primary w-100 py-2" @click="updateProfile">Save Profile Changes</button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'UserDashboard',

    data() {
        return {
            activeTab: 'treks',
            email: localStorage.getItem('email'),
            treks: [],
            bookings: [],

            selectedDifficulty: '',
            selectedLocation: '',
            selectedDuration: '',

            profile: {
              name: '',
              email: '',
              phone: ''
            },
            isExporting: false,
            exportMessage: ''
        }
    },

    methods: {
        logout() {

            localStorage.removeItem('token')
            localStorage.removeItem('role')
            localStorage.removeItem('email')

            this.$router.push('/login')
        },
        async fetchTreks() {

          try {
          
              const token = localStorage.getItem('token')
          
              const response = await axios.get(
                  'http://localhost:5000/api/user/treks',
                  {
                      headers: {
                          Authorization: `Bearer ${token}`
                      }
                  }
              )
                
              this.treks = response.data
                
          }
        
          catch (error) {
          
              console.error(error)
          
              alert('Failed to load treks')
          }
        },
        async bookTrek(trekId) {

          try {
          
              const token = localStorage.getItem('token')
          
              const response = await axios.post(
                  `http://localhost:5000/api/user/book-trek/${trekId}`,
                  {},
                  {
                      headers: {
                          Authorization: `Bearer ${token}`
                      }
                  }
              )
                
              alert(response.data.message)
                
              this.fetchTreks()
                
          }
        
          catch (error) {
          
              alert(
                  error.response?.data?.message ||
                  'Booking failed'
              )
          
              console.error(error)
          }
        },
        async fetchBookings() {

          try {
          
              const token = localStorage.getItem('token')
          
              const response = await axios.get(
                  'http://localhost:5000/api/user/my-bookings',
                  {
                      headers: {
                          Authorization: `Bearer ${token}`
                      }
                  }
              )
                
              this.bookings = response.data
                
          }
        
          catch (error) {
          
              console.error(error)
          
              alert('Failed to load bookings')
          }
        },
        async fetchProfile() {

          try {
          
              const token = localStorage.getItem('token')
          
              const response = await axios.get(
                  'http://localhost:5000/api/user/profile',
                  {
                      headers: {
                          Authorization: `Bearer ${token}`
                      }
                  }
              )
                
              this.profile = response.data
                
          }
        
          catch (error) {
          
              console.error(error)
          
              alert('Failed to load profile')
          }
        },
        async updateProfile() {

          try {
          
              const token = localStorage.getItem('token')
          
              const response = await axios.put(
                  'http://localhost:5000/api/user/profile',
                  {
                      name: this.profile.name,
                      phone: this.profile.phone
                  },
                  {
                      headers: {
                          Authorization: `Bearer ${token}`
                      }
                  }
              )
                
              alert(response.data.message)
                
          }
        
          catch (error) {
          
              console.error(error)
          
              alert('Failed to update profile')
          }
        },
        async cancelBooking(bookingId) {
                
            try {
            
                const token = localStorage.getItem('token')
            
                const response = await axios.put(
                    `http://localhost:5000/api/user/cancel-booking/${bookingId}`,
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                
                alert(response.data.message)
                
                this.fetchBookings()
                
                this.fetchTreks()
                
            }
        
            catch (error) {
            
                alert(
                    error.response?.data?.message ||
                    'Failed to cancel booking'
                )
            
            }
        
        },
        
        async payBooking(bookingId) {
                
            try {
            
                const token = localStorage.getItem('token')
            
                const response = await axios.put(
                    `http://localhost:5000/api/user/pay-booking/${bookingId}`,
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                )
                
                alert(response.data.message)
                
                await this.fetchBookings()
                
            }
        
            catch (error) {
            
                alert(
                    error.response?.data?.message ||
                    'Payment failed'
                )
            
            }
        
        },

        async exportTrekHistory() {
            this.isExporting = true;
            this.exportMessage = '';

            try {
                const token = localStorage.getItem('token');

                const response = await axios.post(
                    'http://localhost:5000/api/user/export-history',
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );
                
                this.exportMessage = response.data.message;
                
            } catch (error) {
                console.error("Export error:", error);
                this.exportMessage = "Failed to trigger export.";
            } finally {
                this.isExporting = false;
            }
        }

    },

    computed: {

        filteredTreks() {
        
            return this.treks.filter(trek => {
            
                const difficultyMatch =
                    !this.selectedDifficulty ||
                    trek.difficulty === this.selectedDifficulty
            
                const locationMatch =
                    !this.selectedLocation ||
                    trek.location
                        .toLowerCase()
                        .includes(
                            this.selectedLocation.toLowerCase()
                        )
            
                const durationMatch =
                    !this.selectedDuration ||
                    trek.duration_days <= this.selectedDuration
            
                return (
                    difficultyMatch &&
                    locationMatch &&
                    durationMatch
                )
            })
        }
    },

    mounted() {
      this.fetchTreks()

      this.fetchBookings()

      this.fetchProfile()
    }
}
</script>