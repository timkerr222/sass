import streamlit as st

def main(user=None):
    st.title("Welcome to RxTrail")
    st.image("https://www.rxtrail.org/wp-content/uploads/2023/10/rxtrail-logo.svg", width=150)  # Insert the correct logo URL here
    
    st.write("""
    **Empowering Your Pharmacy with Precision and Progress**

    RxTrail is a leading pharmacy business consulting firm, dedicated to advancing the business of pharmacy through innovative technology and data-driven decisions. We offer a wide range of services, including:

    - **340B Program Management**: Comprehensive support for managing compliant and high-performing 340B programs.
    - **Data Services**: Optimization and management of pharmacy data to enhance operational efficiency.
    - **Consulting Services**: Expert advice and strategies for retail pharmacies, hospitals, and healthcare organizations.

    Our mission is to revolutionize the pharmacy sector by bridging the gaps between technology, data, and healthcare, ensuring sustainable growth and transformative care for all our clients.
    """)

    st.write("""
    **Why Choose RxTrail?**
    - **Expertise**: Our team includes Apexus-certified experts and veterans in pharmacy operations.
    - **Innovation**: We leverage cutting-edge technology to provide state-of-the-art solutions.
    - **Customer Focus**: We tailor our services to meet the unique needs of each client, driving efficiency and progress in healthcare.

    **Contact Us**: [Get in touch](https://www.rxtrail.org/contact-us/) to learn how we can support your pharmacy's success.
    """)
   
    #st.markdown("<style>[data-testid='stSidebar']{display:none;}</style>", unsafe_allow_html=True)
if __name__ == "__main__":
    main()
