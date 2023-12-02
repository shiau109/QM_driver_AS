clear all
load 3Q_tomo.mat
QSTd = data;
% QSTd = ones(3,3,3,8)/8; % QSTd(q1,q2,q3,bs);   qi : 1 for X, 2 for Y, 3 for Z
QSTd_ext = zeros(4,4,4,8); % QSTd(q1,q2,q3,bs);   qi : 1 for X, 2 for Y, 3 for Z, 4 for I
QSTd_ext(1:3, 1:3, 1:3, :) = QSTd;
%%%% generate IXX IXY IXZ IYX IYY IYZ...XII III data
QSTd_ext(4, 1:3, 1:3, :) = QSTd(1, 1:3, 1:3, :); 
QSTd_ext(1:3, 4, 1:3, :) = QSTd(1:3, 1, 1:3, :);
QSTd_ext(1:3, 1:3, 4, :) = QSTd(1:3, 1:3, 1, :); 
QSTd_ext(4, 4, 1:3, :) = QSTd(1, 1, 1:3, :);
QSTd_ext(4, 1:3, 4, :) = QSTd(1, 1:3, 1, :); 
QSTd_ext(1:3, 4, 4, :) = QSTd(1:3, 1, 1, :); 
QSTd_ext(4, 4, 4, :) = QSTd(1, 1, 1, :); 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
bit_stream = [0 0 0; 0 0 1; 0 1 0; 0 1 1; 1 0 0; 1 0 1; 1 1 0; 1 1 1];
XYZ_table(:,:,1) = [0 1; 1 0]; % X
XYZ_table(:,:,2) = [0 1i; -1i 0]; % Y
XYZ_table(:,:,3) = [-1 0; 0 1]; % Z
I = [1 0;0 1]; %Identity


lo = zeros(8,8); %density matrix
for q1 = 1:4 %1 for X, 2 for Y, 3 for Z, 4 for I
    for q2 = 1:4
        for q3 = 1:4
            
            
            for bs = 1:8
                %%%%%%%%%%%%% q1
                if(q1==4)% 4 for q1's I measurement
                    q1_M = I;
                    eig_q1_M = 1;
                else
                    q1_M = XYZ_table(:,:,q1);
                    eig_q1_M = (-1)^(1-bit_stream(bs, 1));
                end
                
                %%%%%%%%%%%%% q2
                if(q2==4)% 4 for q2's I measurement
                    q2_M = I;
                    eig_q2_M = 1;
                else
                    q2_M = XYZ_table(:,:,q2);
                    eig_q2_M = (-1)^(1-bit_stream(bs, 2));
                end
                
                %%%%%%%%%%%%% q3
                if(q3==4)% 4 for q3's I measurement
                    q3_M = I;
                    eig_q3_M = 1;
                else
                    q3_M = XYZ_table(:,:,q3);
                    eig_q3_M = (-1)^(1-bit_stream(bs, 3));
                end
                
                %%%%%%%%%%%%%%%%%%%%%%
                q1q2q3_M = kron(q1_M,kron(q2_M,q3_M));
                eig_q1q2q3_M = eig_q1_M*eig_q2_M*eig_q3_M;
                lo = lo+eig_q1q2q3_M*QSTd_ext(q1,q2,q3,bs)*q1q2q3_M;
            end% for bs = 1:8
            
            
        end%for q3 = 1:4
    end%for q2 = 1:4
end%for q1 = 1:4
lo = lo/(2^3);
bar3(abs(lo))