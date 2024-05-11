import streamlit as st # pip install streamlit
import time
import os
import pandas as pd
import plotly.express as px # pip install plotly-express
from datetime import datetime
from selenium import webdriver # pip install selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from glob import glob


class RealDiscountUdemyCoursesCouponCodeScraper:
    def __init__(self):
        self.url = "https://www.real.discount/udemy-coupon-code/"
        self.driver = None
        
    def load_webpage(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(5)
        self.driver.get(self.url)
        self.driver.get(self.url)
        
        
    # Call the previous function before calling this function
    def scrape_coupons(self):
        
        try:
            # COUPONS DATA SCRAPED AND RETURNED
            COUPONS_DATA_AND_LABEL = []
            coupons_data_list_list = [] # declaration of list of courses data as list of list
            header = ["title","course","category","provider","duration","rating","language","students_enrolled","price_discounted","price_original","views"]
            courses_container = self.driver.find_element(By.CLASS_NAME, 'list-unstyled')
            courses = courses_container.find_elements(By.TAG_NAME, "a")
            for course in reversed(courses):
                if 'https://www.real.discount' not in course.get_attribute('href'):
                    continue  # Skip ad elements
                
                if 'https://www.real.discount/ads/' in course.get_attribute('href'):
                    continue # Skip ad elements
                coupon_data_list = []
                coupon_data_list.append(course.find_element(By.TAG_NAME, 'h3').text.strip())
                coupon_data_list.append(course.get_attribute('href'))
                coupon_data_list.append(course.find_element(By.TAG_NAME, 'h5').text.strip())
                coupon_data_list.append(course.find_element(By.CSS_SELECTOR, '.p-2:nth-child(1) .mt-1').text.strip())
                coupon_data_list.append(course.find_element(By.CSS_SELECTOR, '.p-2:nth-child(2) .mt-1').text.strip())
                coupon_data_list.append(course.find_element(By.CSS_SELECTOR, '.p-2:nth-child(3) .mt-1').text.strip())
                coupon_data_list.append(course.find_element(By.CSS_SELECTOR, '.p-2:nth-child(4) .mt-1').text.strip())
                coupon_data_list.append(course.find_element(By.CSS_SELECTOR, '.p-2:nth-child(5) .mt-1').text.strip())
                coupon_data_list.append(course.find_element(By.TAG_NAME, 'span').text.strip())
                coupon_data_list.append(course.find_element(By.CLASS_NAME, 'card-price-full').text.strip())
                coupon_data_list.append(course.find_element(By.CSS_SELECTOR, '.p-2:nth-child(7) .ml-1').text.strip())
                coupons_data_list_list.append(coupon_data_list)
            
            COUPONS_DATA_AND_LABEL = [header, coupons_data_list_list] # Data i need to convert to dataframe for comparison and saving
            
            return COUPONS_DATA_AND_LABEL
        
        
        except NoSuchElementException:
            return None

    def close_driver(self):
        self.driver.quit()
        
        
class Dashboard:
    def __init__(self):
        self.title = ":bar_chart: Real-Time Udemy Course Discounts Scraper Dashboard"
        self.df = None
        self.df_selected = None
        self.current_file = None
        today = datetime.now().strftime("%Y-%m-%d")
        today_df = pd.read_csv(f"coupon_courses_{today}.csv")
        self.today_coupons_to_apply_df = today_df
        self.df_selected_df_with_price_original_clearned = None
    
    # set page settings
    def set_settings_session(self):
        st.set_page_config(page_title="Real-Time Udemy Course Discounts Scraper", page_icon=":bar_chart:",layout="wide") # General configuration settings
    
    # -------SIDEBAR--------
    # Filterable variables
    # category,provider,duration,rating,language,students_enrolled,price_discounted,price_original,views, current_date
    def set_sidebar_session(self):
        st.sidebar.header("Choose your filter: ")
        # Current date 
        current_date = ""
        options = glob("*.csv")
        today = datetime.now().strftime("%Y-%m-%d")
        
        self.current_file = st.sidebar.multiselect(
            label="Select the file of your choice based on the date:",
            options= options, 
            default = f"coupon_courses_{today}.csv", 
            help = "Select one or more options."
            )
        
        if self.current_file:
            if len(self.current_file) == 1:
                self.df = pd.read_csv(self.current_file[0])
                st.write(self.df.shape)
            else:
                self.df = pd.read_csv(self.current_file[0])
                for i in range(1, len(self.current_file)):  # Removed unnecessary arguments in range()
                    new_df = pd.read_csv(self.current_file[i])
                    self.df = pd.concat([self.df, new_df], ignore_index=True)  # Append new dataframe to original dataframe
                    st.write(self.df.shape)
                    
            category = st.sidebar.multiselect(
                label="Select your favorite category(ies)",
                options= self.df['category'].unique(), 
                default = self.df['category'].unique(),
                help = "Select one or more options."
                )
            duration = st.sidebar.multiselect(
                label="Select your favorite duration(s)",
                options= self.df['duration'].unique(),
                default = self.df['duration'].unique(),
                help = "Select one or more options."
                )
            provider = st.sidebar.multiselect(
                label="Select your favorite provider(s)",
                options= self.df['provider'].unique(),
                default= self.df['provider'].unique(), 
                help = "Select one or more options."
                )
            rating = st.sidebar.multiselect(
                label="Select your favorite rating(s)",
                options= self.df['rating'].unique(),
                default = self.df['rating'].unique(),
                help = "Select one or more options."
                )
            language = st.sidebar.multiselect(
                label="Select your favorite language(s)",
                options= self.df['language'].unique(),
                default = self.df['language'].unique(), 
                help = "Select one or more options."
                )
            students_enrolled = st.sidebar.multiselect(
                label="Select your favorite students_enrolled",
                options= self.df['students_enrolled'].unique(),
                default = self.df['students_enrolled'].unique(), 
                help = "Select one or more options."
                )
            price_discounted = st.sidebar.multiselect(
                label="Select your favorite price_discounted",
                options= self.df['price_discounted'].unique(),
                default = self.df['price_discounted'].unique(), 
                help = "Select one or more options."
                )
            price_original = st.sidebar.multiselect(
                label="Select your favorite price_original(s)",
                options= self.df['price_original'].unique(),
                default = self.df['price_original'].unique(), 
                help = "Select one or more options."
                )
            views = st.sidebar.multiselect(
                label="Select your favorite view(s)",
                options= self.df['views'].unique(),
                default = self.df['views'].unique(), 
                help = "Select one or more options."
                )
            
                
            # Quering the pandas dataFrame with available options
            self.df_selected = self.df.query(
                "category == @category & duration == @duration & provider == @provider & rating == @rating & language == @language & students_enrolled == @students_enrolled & price_discounted == @price_discounted & price_original == @price_original & views == @views"
            )
            
            # Check if the df_selected is empty
            if self.df_selected.empty:
                st.warning("No data available based on the current filter settings!")   
        else:
            st.title(self.title)
            st.markdown("##")
            st.markdown("""---""")
            st.subheader("No file selected, so please select a file based on your favorite date")  
                        
                            
            
    # -----------MAIN PAGE--------------
    def set_title_session(self):
        st.title(self.title)
        st.markdown("##")
    
    
    # st.markdown("""---""")
    
    # Show the selected course file dates  
    def set_date_selected_session(self):    
        if len(self.current_file) == 1:
            current_date = str(self.current_file[0])[15:25]
            st.subheader("Current date: **" + current_date + "**")
                    
        elif len(self.current_file) > 1:
            # st.subheader("Current dates: ")
            dates = ""
            for item in range(len(self.current_file)):
                current_date = str(self.current_file[item])[15:25]
                dates += "**" + current_date + "**, "
            dates = dates[:-2]  # Remove the last comma and space
            # st.markdown(dates)
            st.subheader("Current date: **" + dates + "**")

        else:
            st.subheader("No file selected, so please select a file based on your favorite date")
            
    # st.markdown("""---""")


    def set_courses_prices_statics_session(self):
        self.df_selected_df_with_price_original_clearned = self.df_selected.copy()
        self.df_selected_df_with_price_original_clearned['price_original'] = self.df_selected_df_with_price_original_clearned['price_original'].str.replace('$', '').astype(float)
        # TOP KPI'S
        total_original_courses_price = round(self.df_selected_df_with_price_original_clearned['price_original'].sum(),3) # Total original courses price for selected course
        average_rating = round(self.df_selected['rating'].astype(float).mean(), 1) # Average rating for selected course
        star_rating =":star:" * int(round(average_rating, 0)) # Star rating for selected course
        average_original_courses_price = round(self.df_selected_df_with_price_original_clearned['price_original'].mean(),3) # Average original courses price for selected course
        
        start_column, middle_column, end_column = st.columns(3)
        
        with start_column:
            st.subheader("Total Original Courses Price:")
            st.subheader(f"US $ {total_original_courses_price:,}")
        with middle_column:
            st.subheader("Average Rating:")
            st.subheader(f"{average_rating} {star_rating}")
        with end_column:
            st.subheader("Average Original Courses Price:")
            st.subheader(f"US $ {average_original_courses_price}")
            
    
    # Show pandas data frame session
    def show_data_table_session(self):
        # st.markdown("""---""")
        
        show_table = st.checkbox("Show your filtered data as a table")
        if show_table:
            st.table(self.df_selected) # Show all courses selected here
     
    # Display Coupon code courses in order to allow users to choose a course and apply the coupon code        
    def coupon_code_courses_application_session(self):
        
        
        for index, row in self.today_coupons_to_apply_df.iterrows():
            title_column, link_column = st.columns(2)
            with title_column:
                st.subheader(row['title'])
            with link_column:
                st.link_button("Apply", row['course'])
                
    # Dashboard functionality
    
    def price_original_by_category_bar_chart_dashboard(self):
        # Originale Price BY Category LINE [BAR CHART]
        price_original_by_category_line = self.df_selected_df_with_price_original_clearned.groupby(by=["category"])[["price_original"]].sum().sort_values(by="price_original")
        st.subheader("Price Original by Category Line")
        fig_category_price_original = px.bar(
            price_original_by_category_line,
            x="price_original",
            y=price_original_by_category_line.index,
            orientation="h", # Horizontal
            height=1000, 
            width = 1000,
            # title="<b>Price Original by Category Line</b>",
            color_discrete_sequence=["#0083B8"] * len(price_original_by_category_line),
            template="plotly_white",
        )
        fig_category_price_original.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )
        # BAR CHAT
        st.plotly_chart(fig_category_price_original, use_container_width=True)

    
    
    def price_original_by_language_bar_chart_dashboard(self):
        # Originale Price BY Language LINE [BAR CHART]
        price_original_by_language_line = self.df_selected_df_with_price_original_clearned.groupby(by=["language"])[["price_original"]].sum()
        st.subheader("Price Original by Language Line")
        fig_language_price_original = px.bar(
            price_original_by_language_line,
            x=price_original_by_language_line.index,
            y="price_original",
            height=500, 
            width = 1000,
            # title="<b>Price Original by Language Line</b>",
            color_discrete_sequence=["#0083B8"] * len(price_original_by_language_line),
            template="plotly_white",
        )
        fig_language_price_original.update_layout(
            xaxis=dict(tickmode="linear"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False)),
        )

        # BAR CHAT
        st.plotly_chart(fig_language_price_original, use_container_width=True)
        
        
        
        
    def price_original_by_language_pie_chart_dashboard(self):
        price_original_by_language_pie = self.df_selected_df_with_price_original_clearned.groupby(by=["language"])[["price_original"]].sum()
        st.subheader("Price Original by Language")
        fig = px.pie(price_original_by_language_pie, values="price_original", names=price_original_by_language_pie.index)
        st.plotly_chart(fig, use_container_width=True)
                
        
    
        
        
    
    def hide_streamlit_style_session(self):
        # ---- HIDE STREAMLIT STYLE ----
        hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_st_style, unsafe_allow_html=True)
    
            

            


def main():
    
    ### DASHBOARD ###
    
    scraper = RealDiscountUdemyCoursesCouponCodeScraper()
    
    scraper.load_webpage()
    scraped_data = scraper.scrape_coupons()
    if scraped_data:
        header, new_courses = scraped_data
        display_new_courses(header, new_courses)
    else:
        st.write("No coupons found at the moment.")
        
    scraper.close_driver()
    
    
    scraper.load_webpage()
    
    dashboard = Dashboard()
    
    dashboard.set_settings_session()
   
    dashboard.set_sidebar_session()
    
    dashboard.set_title_session()
    
    st.markdown("""---""")
    
    dashboard.set_date_selected_session()
    
    st.markdown("""---""")
    
    dashboard.set_courses_prices_statics_session()
    
    st.markdown("""---""")
    
    dashboard.show_data_table_session()
    
    st.markdown("""---""")
    
    dashboard.price_original_by_category_bar_chart_dashboard()
    
    st.markdown("""---""")
    
    dashboard.price_original_by_language_bar_chart_dashboard()
    
    st.markdown("""---""")
    
    dashboard.price_original_by_language_pie_chart_dashboard()
    
    st.markdown("""---""")
    
    st.subheader("Apply to all available coupons courses codes here")
    
    st.markdown("""---""")
    
    dashboard.coupon_code_courses_application_session()
    
    st.markdown("""---""")
    
    dashboard.hide_streamlit_style_session()
    
    # ------------- Real Time Streaming Coupon code scraping from web -------------------------------- 

    
    
    while True:
        
        scraper.load_webpage()
        scraped_data = scraper.scrape_coupons()
        if scraped_data:
            header, new_courses = scraped_data
            new_df = display_new_courses(header, new_courses)
            dashboard.today_coupons_to_apply_df = new_df
        else:
            st.write("No coupons found at the moment.")
            
        scraper.close_driver()
        # Sleep for 1 hour before scraping again
        time.sleep(300)  # 5 * 60 seconds = 5 minutes
    
    scraper.close_driver()
    



def display_new_courses(header, new_courses):
    try:
        existing_courses = pd.read_csv(get_today_csv_filename(), header=0).iloc[:, 1].tolist()

        # print(existing_courses)
    except FileNotFoundError:
        existing_courses = []
    
    new_courses = [course for course in new_courses if course[1] not in existing_courses]
    if new_courses:
        save_to_csv(new_courses,header)
        # st.write("Available New Udemy Course Coupons:")
        new_df = pd.DataFrame(new_courses, columns=header)
        return new_df
        # st.write(df)


def save_to_csv(new_courses, header):
    filename = get_today_csv_filename()
    
    # Check if the file exists
    if not os.path.isfile(filename):
        # If the file doesn't exist, write the header
        df = pd.DataFrame(columns=header)  # Create an empty DataFrame with the header
        df.to_csv(filename, index=False)   # Write the header to the CSV file
    
    # Append the new data without the header
    df = pd.DataFrame(new_courses, columns=header)
    df.to_csv(filename, mode='a', header=False, index=False)


def get_today_csv_filename():
    today = datetime.now().strftime("%Y-%m-%d")
    return f"coupon_courses_{today}.csv"


if __name__ == "__main__":
    main()
