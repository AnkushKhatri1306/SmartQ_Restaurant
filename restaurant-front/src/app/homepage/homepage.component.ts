import { Component, OnInit } from '@angular/core';
import { RestaurantService } from '../__service/restaurant.service';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {

  constructor(private resService: RestaurantService) { }

  restaurantList: any;
  restuarantLocation: any;
  restaurantDetail: any;
  responseData: any;
  searchStr: any;
  page:any;
  per_page:any;
  sortSelected:any = "";
  openPopup: boolean = false;

  ngOnInit() {
    this.getRestaurantListData();
  }

  searchRestaurant(text){
    this.searchStr = text;
    this.getRestaurantListData();
  }

  getPage(page){
      this.page = page;
      console.log(page);
      this.getRestaurantListData();
  }

  getRestaurantListData(){
    let data = {}
    data['page_no'] = this.page || 1;
    data['per_page'] = this.per_page || 15;
    data['search_str']= this.searchStr;
    data['sort'] = this.sortSelected;
    this.resService.getRestaurantList(data).subscribe(resp => {
      if(resp.status == 'success'){
          this.restaurantList = resp.data.result;
          this.responseData = resp.data;
          console.log(this.restaurantList, 'ass', resp);
          
      }
    },
    error => {

    })
  }

  displayRestaurantDetail(rest){
    this.restaurantDetail = rest;
    console.log('red')
    this.resService.getLocationDetail(rest.id).subscribe(resp => {
      if(resp.status == 'success'){          
          this.restuarantLocation = resp.data;
          console.log(this.restuarantLocation);
          this.restuarantLocation.latitude = parseFloat(this.restuarantLocation.latitude);
          this.restuarantLocation.longitude = parseFloat(this.restuarantLocation.longitude);
          this.openPopup = true;
      }
    },
    error => {

    })
  }

}
