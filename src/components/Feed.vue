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
                <md-radio v-model="rating" value="0">Strongly Left</md-radio>
                <md-radio v-model="rating" value="1">Left</md-radio>
                <md-radio v-model="rating" value="2">Centre</md-radio>
                <md-radio v-model="rating" value="3">Right</md-radio>
                <md-radio v-model="rating" value="4">Strongly Right</md-radio>
              </div>
            </md-card-content>

            <md-card-expand-trigger>
              <md-button>Submit</md-button>
            </md-card-expand-trigger>

            <md-card-expand-content>
              <!-- If left -->
              <md-card-content>
                Correctly identified. We'd however recommend looking at other perspectives as well!
              </md-card-content>
              <md-button class="md-accent" v-on:click="submitRating">Got it</md-button>
            </md-card-expand-content>


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
                  <md-radio v-model="rating" value="1">Fake</md-radio>
                  <md-radio v-model="rating" value="0">Not fake</md-radio>
                </div>
              </md-card-content>


              <md-card-expand-trigger>
                <md-button>Submit</md-button>
              </md-card-expand-trigger>

              <md-card-expand-content>
                <!-- If correct -->
                <md-card-content v-if="rating === currentCard['vfake'] || rating === currentCard['hfake']">
                  Correctly identified. You have got it!
                </md-card-content>
                <!-- If FN - headline works -->
                <md-card-content v-else-if="rating !== currentCard['hfake'] && currentCard['hfake'] === '1'
                && currentCardType === 'H'">
                  That is fake news actually. For identifying fake news, DO NOT form an opinion just on the
                  headline, but also look at the publication (it could be satirical) and whether the headline agrees with
                  the content of the article.
                </md-card-content>

                <!-- If FP - headline -->
                <md-card-content v-else-if="rating !== currentCard['hfake'] && currentCard['hfake'] === '0'
                && currentCardType === 'H'">
                  That headline is actually true. Usually, reputable sources with factual information publish accurate
                  stories.
                </md-card-content>

                <md-card-content v-else-if="rating !== currentCard['vfake'] && currentCard['vfake'] === '1'
                && currentCardType === 'V'">
                  This is a deepfake!
                  <md-list>
                    <md-list-item>Pay attention to the face.</md-list-item>
                    <md-list-item>Pay attention to the eyes and eyebrows. </md-list-item>
                    <md-list-item>DeepFakes often fail to fully represent the natural physics of lighting.</md-list-item>
                  </md-list>
                </md-card-content>

                <md-card-content v-else>
                  That's not correct. If it sounds too incredulous and ridicules someone, there is a high probability it
                  is satirical!
                </md-card-content>

                <md-button class="md-accent" v-on:click="submitRating">Got it</md-button>
              </md-card-expand-content>

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
        let event = {
          "user_id": "100",
          "card_id": this.currentCard["CARDID"],
          "rating": this.rating,
          "type": this.currentCardType,
          "leaning": this.currentCard["leaning"],
          "isfake": this.currentCardType === "V" ? this.currentCard["vfake"] : this.currentCard["hfake"]
        }

        this.userInteractionEvents.push(event);

        let nextCard = this.currentCardIndex + 1;

        if (nextCard !== (this.feedElements).length) {
          this.currentCard = this.feedElements[nextCard];
          this.currentCardIndex = this.currentCardIndex+1;
          this.currentCardType = this.feedElements[this.currentCardIndex].CARDTYPE;
        }

        else {
          this.reachedEndOfFeed = true;
          this.currentCardIndex = 0;
          this.currentCard = null;
          this.postToDb(this.userInteractionEvents);
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

            if (card["CARDTYPE"] === 'V') {
              this.feedElements[index].vfake = this.feedElements[index].vfake ? "1" : "0";
            }

            if (card["CARDTYPE"] === 'H') {
              this.feedElements[index].hfake = this.feedElements[index].hfake ? "1" : "0";
            }
            console.log(card);
          })


        }
      },
      postToDb: async function(userInteractionEvents) {
        console.log(userInteractionEvents)
        let result = await axios.post(`http://127.0.0.1:5000/postevent`, {userInteractionEvents});
        let test = await axios.post(`http://127.0.0.1:5000/postevent/${userInteractionEvents}`);
        if (result.status !== 200 || test) {
          this.postFailed = false;
        }
      }
    }
    }
</script>