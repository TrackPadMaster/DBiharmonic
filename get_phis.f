
	  IMPLICIT REAL*8 (A-H,O-Z)
	  IMPLICIT INTEGER*4 (I-N)
          real*8 x(1000)

      np=22
      pi= 3.141592653589793d0
      dx=2.d0*pi/(np)
      do i=1,np
        xx=dx*dble(i-1)
        x(i)=xx
      enddo
      print 222,(x(i),i=1,np)
     
 222  format(1000(f20.13))
      end

