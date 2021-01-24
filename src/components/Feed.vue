<template>
  <div>
    <div class="md-layout">
      <div class="md-layout-item"></div>
      <div class="md-layout-item md-size-50">
        <div :key="currentCardIndex" v-if="currentCard" >

          <!-- News card -->
          <md-card v-if="currentCardType === 'P'">
            <md-card-header>
              <div class="md-title">{{ currentCard["opheadline"] }}</div>
              <!--          <div class="md-subhead">{{feedElements[currentCard].friends_interactions}}</div>-->
            </md-card-header>

            <md-card-content>
              <a :href = "currentCard['opinion_source']">{{ currentCard["opinion_source"] }}</a>
              <h3 class="md-subheading">Where do you think this article lies on the political spectrum?</h3>
              <div class="rating-spectrum">
                <md-radio v-model="rating" value="sLeft">Strongly Left</md-radio>
                <md-radio v-model="rating" value="Left">Left</md-radio>
                <md-radio v-model="rating" value="Centre">Centre</md-radio>
                <md-radio v-model="rating" value="Right">Right</md-radio>
                <md-radio v-model="rating" value="sRight">Strongly Right</md-radio>
              </div>
            </md-card-content>

            <md-button v-on:click="submitRating">Submit</md-button>

          </md-card>
          <!-- News card -->
          <!-- Video -->
          <div v-else>
            <md-card >
              <md-card-header>
                <div v-if="currentCardType === 'V'"
                     class="md-title">Is this video fake?</div>
                <div v-else>
                  <div  class="md-title"> Is this a fake headline?</div>
                  <h3>{{ currentCard["fheadline"] }}</h3>
                  <h4>Outlet: <span>{{ currentCard["newsoutlet"] }} </span></h4>
                </div>

                <div class="md-subhead">Select Fake/Not Fake to proceed</div>
              </md-card-header>

              <md-card-media md-big>
                <!-- Todo add video link -->
                <!--          <img src="/assets/examples/avatar-2.jpg" alt="People">-->

                <div v-if="currentCardType === 'V'">
                  <youtube-media player-height="640" player-width="450" v-if="currentCardType === 'V'"
                                 :video-id="currentCard['video_id']"></youtube-media>
                </div>
              </md-card-media>

              <md-card-content>
                <!--          <div v-if="currentCardType === 'fake_headline'">-->
                <!--            <h2>{{feedElements[currentCard].headline}}</h2>-->
                <!--          </div>-->

                <div class="rating-spectrum">
                  <md-radio v-model="rating" :value=1>Fake</md-radio>
                  <md-radio v-model="rating" :value=0>Not fake</md-radio>
                </div>
              </md-card-content>


              <md-button v-on:click="submitRating" class="md-raised md-accent">Submit</md-button>

            </md-card>
            <!-- Video // Fake Headline -->

          </div>


        </div>
        <div v-else>You have reached the end of your feed, check back later :)</div>

      </div>
      <div class="md-layout-item"></div>
      </div>
    </div>

</template>

<style lang="scss" scoped>
  .md-card {
    border-radius: 4px;
    padding: 0 !important;
  }

  md-card-media {
    height: 75% !important;
  }

</style>

<script>
import axios from 'axios';
import {getIdFromURL} from 'vue-youtube-embed';

async function fetchFeedElements(callback) {
    try {
      let elements = await axios.get(`http://127.0.0.1:5000/feed`);
      callback(null, elements);
    } catch (e) {
      callback(e, null);
      console.log(e);
    }
  }

  export default {
    name: "Feed",
    data: () => ({
      feedElements: null,
      currentCardType: null,
      currentCardIndex: 0,
      currentCard: null,
      reachedEndOfFeed: false,
      rating: null,
      cardUpdated: 'no',
      userInteractionEvents: [],
      error: null,
    }),

    created() {

      fetchFeedElements((err, feedElements) => {
        this.setData(err, feedElements);
      })


    },

    methods: {
      submitRating: function () {
        // let event = {
        //   "user_id": "User 1",
        //   "item_id": this.feedElements[this.currentCardIndex].id,
        //   "rating": this.rating
        // }
        //
        // this.userInteractionEvents.push(event);
        let nextCard = this.currentCardIndex + 1;
        if (nextCard !== (this.feedElements).length) {
          this.currentCard = this.feedElements[nextCard];
          this.currentCardType = this.feedElements[nextCard].type;
          this.currentCardIndex = this.currentCardIndex+1;


        }

        else {
          this.reachedEndOfFeed = true;
          this.currentCard = null;
          // TODO send interaction events to database
        }
      },

      setData(err, feedElements) {
        if (err) {
          this.error = err.toString;
          console.log(this.error);
        } else {
          this.feedElements = feedElements.data;
          this.currentCardType = this.feedElements[this.currentCardIndex].CARDTYPE;
          this.currentCard = this.feedElements[this.currentCardIndex]
          this.feedElements.forEach((card, index) => {
            if (card["CARDTYPE"] === 'V') {
              this.feedElements[index].video_id = getIdFromURL(card["sourcelink"])
            }
          })
        }
      }
    }
  }
</script>