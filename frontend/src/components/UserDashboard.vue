<template>
    <div>

        <h1>User Dashboard</h1>

        <p>Welcome {{ email }}</p>

        <button @click="logout">Logout</button>

        <hr>

        <button @click="activeTab = 'treks'">Available Treks</button>

        <button @click="activeTab = 'bookings'">My Bookings</button>

        <button @click="activeTab = 'profile'">Profile</button>

        <hr>

        <div v-if="activeTab === 'treks'">

          <h2>Available Treks</h2>
          <hr>

          <label>Difficulty:</label>

          <select v-model="selectedDifficulty">
          
              <option value="">All</option>
          
              <option value="Easy">Easy</option>
          
              <option value="Moderate">Moderate</option>
          
              <option value="Hard">Hard</option>
          
          </select>

          <br><br>

          <label>Location:</label>

          <input type="text" v-model="selectedLocation" placeholder="Search Location"/>

          <br><br>

          <label>Maximum Duration:</label>

          <input type="number" v-model="selectedDuration"/>

          <hr>

          <div v-for="trek in filteredTreks" :key="trek.id">
          
              <h3>{{ trek.trek_name }}</h3>
          
              <p>Location: {{ trek.location }}</p>
          
              <p>Difficulty: {{ trek.difficulty }}</p>
          
              <p>Duration: {{ trek.duration_days }} Days</p>
          
              <p>Available Slots: {{ trek.available_slots }}</p>
          
              <p>Price: ₹{{ trek.price }}</p>

              <button @click="bookTrek(trek.id)">Book Trek</button>
          
              <hr>
          
          </div>
        
        </div>

        <div v-if="activeTab === 'bookings'">

          <h2>My Bookings</h2>

          <div v-for="booking in bookings" :key="booking.id">
        
            <h3>{{ booking.trek_name }}</h3>
        
            <p><strong>Location:</strong> {{ booking.location }}</p>
        
            <p><strong>Start Date:</strong> {{ booking.start_date }}</p>
        
            <p><strong>End Date:</strong> {{ booking.end_date }}</p>
        
            <p><strong>Status:</strong> {{ booking.status }}</p>
        
            <p><strong>Payment:</strong> {{ booking.payment_status }}</p>
        
            <p><strong>Booking Date:</strong> {{ booking.booking_date }}</p>
        
            <button v-if="booking.status === 'Booked'" @click="cancelBooking(booking.id)">Cancel Booking</button>
        
            <hr>
        
          </div>
      
        </div>

        <div v-if="activeTab === 'profile'">

          <h2>Profile</h2>

          <div>
            <label>Name:</label>
            <input type="text" v-model="profile.name">
          </div>
        
          <br>
        
          <div>
            <label>Email:</label>
            <input type="email" v-model="profile.email" readonly>
          </div>
        
          <br>
        
          <div>
            <label>Phone:</label>
            <input type="text" v-model="profile.phone">
          </div>

          <br><br>

          <button @click="updateProfile">Save Profile</button>
        
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
            }
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